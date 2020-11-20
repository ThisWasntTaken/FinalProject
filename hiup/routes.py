from flask import render_template, url_for, flash, redirect, request, make_response, jsonify
from hiup.models import User, Patient, Consent, Encounter, Record, Request_Log, Access_Log
from hiup.forms import RegistrationForm, LoginForm, ConsentForm, DataRequestForm, CreateTeamForm
from hiup import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import requests
import json
import base64
from datetime import datetime, time
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from utils import *
from policies import *

@app.route('/', methods = ['GET', 'POST'])
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    else:
        return render_template('login.html', title = 'Login', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(digi_doctor_id = form.digi_doctor_id.data if form.digi_doctor_id.data else None, name = form.name.data, email = form.email.data, phone = form.phone.data, user_type = USER_TYPE_MAP[form.user_type.data], password = password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('register.html', title = 'Register', form = form)

@app.route('/create_team', methods = ['GET', 'POST'])
@login_required
def create_team():
    if current_user.user_type != UserType.ADMIN:
        flash(f'You do not have access to that page.', 'danger')
        return redirect(url_for('home'))
    
    form = CreateTeamForm()
    if request.method == 'POST' and form.validate_on_submit():
        consent = Consent.query.filter_by(id = form.consent_id.data).first()
        if not consent.status == StatusType.ACCEPTED or consent.derived_from is not None:
            flash(f'That consent is not available at this time.', 'danger')
            return render_template('create_team.html', title = 'Create Team', form = form)
        
        for i in [form.id_1.data, form.id_2.data]:
            if i and i != consent.user_id:
                derived = Consent(
                    derived_from = consent.id,
                    user_id = i,
                    patient_id = consent.patient_id,
                    hip_id = consent.hip_id,
                    artefact = consent.artefact,
                    signature = consent.signature,
                    status = StatusType.ACCEPTED
                )
                db.session.add(derived)
                db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('create_team.html', title = 'Create Team', form = form)

@app.route('/consent_request', methods = ['GET', 'POST'])
@login_required
def consent_request():
    form = ConsentForm()
    if request.method == 'POST' and form.validate_on_submit():
        patient = Patient.query.filter_by(health_id = form.health_id.data).first()
        consent = Consent(
                            derived_from = None,
                            user_id = current_user.id,
                            patient_id = patient.id,
                            hip_id = form.hip_id.data,
                            artefact = None,
                            signature = None,
                            status = StatusType.ACTIVE
                        )
        db.session.add(consent)
        db.session.commit()
        data = {'request_id' : consent.id,
                'health_id' : form.health_id.data,
                'hiu_id' : app.config['HIU_ID'],
                'requester_name' : current_user.name,
                'hip_id' : form.hip_id.data,
                'purpose' : form.purpose.data,
                'time_from' : str(form.time_from.data),
                'time_to' : str(form.time_to.data)
        }
        if form.encounter_id.data:
            data['encounter_id'] = form.encounter_id.data
        if form.record_id.data:
            data['record_id'] = form.record_id.data
        response = requests.post('http://127.0.0.1:5000/get_consent_request', json = data)
        flash(f'Your consent request has been sent to the patient.', 'success')
        return redirect(url_for('home'))
    else:
        return render_template('consent_request.html', title = 'Consent', form = form)

def check_constraints(patient, artefact, signature, purpose, user_type):
    h = SHA256.new(artefact)
    verifier = pss.new(RSA.import_key(patient.public_key))
    try:
        verifier.verify(h, signature)
    except:
        return False
    
    artefact = json.loads(artefact)
    time_from = datetime.strptime(artefact['time_from'], '%Y-%m-%d %H:%M:%S').date()
    time_to = datetime.strptime(artefact['time_to'], '%Y-%m-%d %H:%M:%S').date()
    if purpose in [PURPOSE_MAP[artefact['purpose']], PurposeType.ROUNDS]\
    and time_from <= datetime.now().date() <= time_to\
    and purpose in USERTYPE_ACTIVITY_MAP[user_type]:
        return True
    
    return False

@app.route('/data_request', methods = ['GET', 'POST'])
@login_required
def data_request():
    form = DataRequestForm()
    consents = Consent.query.filter_by(status = StatusType.ACCEPTED).all()
    consents += Consent.query.filter_by(status = StatusType.CACHED).all()
    form.consent_id.choices = [(i.id, str(i)) for i in consents]
    if request.method == 'POST' and form.validate_on_submit():
        consent = Consent.query.filter_by(id = int(form.consent_id.data)).first()
        patient = Patient.query.filter_by(id = consent.patient_id).first()
        artefact = consent.artefact
        signature = consent.signature
        ret = None
        request_log = Request_Log(consent_id = consent.id, time = datetime.now(), purpose = PURPOSE_MAP[form.purpose.data])
        db.session.add(request_log)
        db.session.commit()
        if not(consent.user_id == current_user.id or check_on_duty()):
            flash(f"You do not have the permission to perform data requests at this time.", "danger")
        else:
            derived = Consent(
                derived_from = consent.id,
                user_id = current_user.user_id,
                patient_id = consent.patient_id,
                hip_id = consent.hip_id,
                artefact = consent.artefact,
                signature = consent.signature,
                status = StatusType.ACCEPTED
            )
            db.session.add(derived)
            db.session.commit()
        
        if not check_constraints(patient, artefact, signature, PURPOSE_MAP[form.purpose.data], current_user.user_type):
            flash(f"Invalid request, constraints not satisfied.", "danger")
        
        if consent.hip_id == int(app.config['HIP_ID']) or consent.status == StatusType.CACHED:
            data = get_data(artefact.decode('utf-8'), signature, purpose = PURPOSE_MAP[form.purpose.data], hiu_id = app.config['HIU_ID'], user_id = current_user.id, consent = consent)
            ret = json.loads(json.dumps(data))
            if not data:
                return "Data not found"
        else:
            artefact = artefact.decode('utf-8')
            signature = base64.b64encode(signature).decode('utf-8')
            data = {'artefact' : artefact,
                    'signature' : signature,
                    'health_id' : patient.health_id,
                    'hip_id' : consent.hip_id,
                    'purpose' : form.purpose.data,
                    'hiu_id' : app.config['HIU_ID'],
                    'user_id' : current_user.id,
                    'user_type' : INVERSE_USER_TYPE_MAP[current_user.user_type]
            }
            response = requests.post('http://127.0.0.1:5000/get_data_request', json = data)
            if response.status_code != 201:
                return response.text
            
            ret = json.loads(response.text)

        if (not consent.hip_id == int(app.config['HIP_ID'])) and form.cache.data and (not consent.status == StatusType.CACHED):
            consent.status = StatusType.CACHED
            db.session.commit()
            artefact = json.loads(artefact)
            if artefact['encounter_id']:
                encounter = Encounter(patient_id = consent.patient_id)
                db.session.add(encounter)
                db.session.commit()
                for _, d in ret.items():
                    record = Record(encounter_id = encounter.id, patient_id = consent.patient_id, data = d[0], record_type = RECORD_TYPE_MAP[d[1]])
                    db.session.add(record)
                    db.session.commit()

                consent.encounter_id = encounter.id
                db.session.commit()
            else:
                d = list(ret.values())[0]
                record = Record(patient_id = consent.patient_id, data = d[0], record_type = RECORD_TYPE_MAP[d[1]])
                db.session.add(record)
                db.session.commit()
                consent.record_id = record.id
                db.session.commit()

        return ret
    else:
        return render_template('data_request.html', title = 'Consent', form = form)

@app.route('/home')
def home():
    if current_user.is_authenticated:
        if current_user.user_type == UserType.ADMIN:
            return render_template('admin_home.html', title = 'Admin')
        return render_template('home.html', title = 'Home')
    else:
        return redirect(url_for('login'))

@app.route('/consent_listener', methods = ['POST'])
def consent_listener():
    content = request.get_json()
    if content['accept']:
        consent = Consent.query.filter_by(id = content['consent_id']).first()
        patient = Patient.query.filter_by(id = consent.patient_id).first()
        signature = base64.b64decode(content['signature'].encode('utf-8'))
        artefact = content['artefact']
        h = SHA256.new(artefact.encode('utf-8'))
        verifier = pss.new(RSA.import_key(patient.public_key))
        try:
            verifier.verify(h, signature)
            consent.status = StatusType.ACCEPTED
            consent.artefact = artefact.encode('utf-8')
            consent.signature = signature
            db.session.commit()
            return make_response("Received consent status", 201)
        except (ValueError, TypeError):
            return make_response("Invalid Signature", 401)
    else:
        consent = Consent.query.filter_by(id = content['consent_id']).first()
        if consent.status == StatusType.ACCEPTED:
            consent.status = StatusType.REVOKED
            derived_consents = Consent.query.filter_by(derived_from = consent.id)
            for d_c in derived_consents:
                d_c.status = StatusType.REVOKED
        else:
            consent.status = StatusType.DENIED
        db.session.commit()
        return make_response("Received consent status", 201)

def check_on_duty():
    return (current_user.user_type in [UserType.NURSE, UserType.RECEPTIONIST] and time(9, 0, 0, 0) <= datetime.now().time() <= time(21, 0, 0, 0))\
    or (current_user.user_type in [UserType.DOCTOR, UserType.PHARMACIST])

@app.route('/get_data_request', methods = ['POST'])
def get_data_request():
    content = request.get_json()
    patient = Patient.query.filter_by(health_id = content['health_id']).first()
    signature = base64.b64decode(content['signature'].encode('utf-8'))
    artefact = content['artefact']
    h = SHA256.new(artefact.encode('utf-8'))
    verifier = pss.new(RSA.import_key(patient.public_key))
    try:
        verifier.verify(h, signature)
    except:
        return make_response("Invalid Signature", 401)
    
    response = get_data(artefact, signature, PURPOSE_MAP[content['purpose']], int(content['hiu_id']), int(content['user_id']))
    return response

def get_data(artefact, signature, purpose, hiu_id, user_id, consent=None):
    access_log = Access_Log(hiu_id = hiu_id, user_id = user_id, artefact = artefact.encode('utf-8'), signature = signature, time = datetime.now(), purpose = purpose)
    artefact = json.loads(artefact)

    db.session.add(access_log)
    db.session.commit()
    
    if consent and consent.status == StatusType.CACHED or hiu_id == app.config['HIU_ID']:
        data = dict()
        if consent.record_id:
            record = Record.query.filter_by(id = consent.record_id).first()
            if not record:
                return data
            
            data[record.id] = [record.data, INVERSE_RECORD_TYPE_MAP[record.record_type]]
        else:
            records = Record.query.filter_by(encounter_id = consent.encounter_id)
            if not records:
                return data
            
            for record in records:
                data[record.id] = [record.data, INVERSE_RECORD_TYPE_MAP[record.record_type]]
    
        return data
    
    data = dict()
    if 'record_id' in artefact.keys():
        record = Record.query.filter_by(id = artefact['record_id']).first()
        if not record:
            return make_response("Record not found", 404)
        
        data[record.id] = [record.data, INVERSE_RECORD_TYPE_MAP[record.record_type]]
    else:
        records = Record.query.filter_by(encounter_id = artefact['encounter_id'])
        if not records:
            return make_response("Encounter not found", 404)
        
        for record in records:
            data[record.id] = [record.data, INVERSE_RECORD_TYPE_MAP[record.record_type]]
    
    return make_response(json.dumps(data), 201)