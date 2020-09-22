from flask import render_template, url_for, flash, redirect, request, make_response, jsonify
from hiu.models import User, Patient, Consent, UserType, PurposeType
from hiu.forms import RegistrationForm, LoginForm, ConsentForm, DataRequestForm
from hiu import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import requests
from datetime import datetime

PURPOSE_MAP = {"Diagnosis" : PurposeType.DIAGNOSIS, "Prescription" : PurposeType.PRESCRIPTION}
INVERSE_PURPOSE_MAP = {val : key for key, val in PURPOSE_MAP.items()}
USER_TYPE_MAP = {"Doctor" : UserType.DOCTOR, "Nurse" : UserType.NURSE, "Receptionist" : UserType.RECEPTIONIST, "Pharmacist" : UserType.PHARMACIST}
INVERSE_USER_TYPE_MAP = {val : key for key, val in USER_TYPE_MAP.items()}

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
        user = User(digi_doctor_id = form.digi_doctor_id.data, name = form.name.data, email = form.email.data, phone = form.phone.data, user_type = USER_TYPE_MAP[form.user_type.data], password = password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('register.html', title = 'Register', form = form)

@app.route('/consent_request', methods = ['GET', 'POST'])
@login_required
def consent_request():
    form = ConsentForm()
    if request.method == 'POST' and form.validate_on_submit():
        patient = Patient.query.filter_by(health_id = form.health_id.data).first()
        consent = Consent(
                            user_id = current_user.id,
                            patient_id = patient.id,
                            hip_id = form.hip_id.data,
                            record_id = form.record_id.data,
                            purpose = PURPOSE_MAP[form.purpose.data],
                            time_from = form.time_from.data,
                            time_to = form.time_to.data,
                            accept = False
                        )
        db.session.add(consent)
        db.session.commit()
        data = {'request_id' : consent.id,
                'health_id' : form.health_id.data,
                'hiu_id' : app.config['HIU_ID'],
                'requester_name' : current_user.name,
                'hip_id' : form.hip_id.data,
                'record_id' : form.record_id.data,
                'purpose' : form.purpose.data,
                'time_from' : str(form.time_from.data),
                'time_to' : str(form.time_to.data)
        }
        response = requests.post('http://127.0.0.1:5000/get_consent_request', json = data)
        flash(f'Your consent request has been sent to the patient.', 'success')
        return redirect(url_for('home'))
    else:
        return render_template('consent_request.html', title = 'Consent', form = form)

@app.route('/data_request', methods = ['GET', 'POST'])
@login_required
def data_request():
    form = DataRequestForm()
    consents = Consent.query.filter_by(user_id = current_user.id, accept = True)
    form.consent_id.choices = [(i.id, str(i)) for i in consents if i.time_from <= datetime.now() <= i.time_to]
    if request.method == 'POST' and form.validate_on_submit():
        consent = Consent.query.filter_by(id = int(form.consent_id.data)).first()
        consent_dict = {
                            'record_id' : consent.record_id,
                            'purpose' : INVERSE_PURPOSE_MAP[consent.purpose],
                            'time_from' : str(consent.time_from),
                            'time_to' : str(consent.time_to)
                        }
        data = {'consent' : consent_dict,
                'health_id' : form.health_id.data,
                'hip_id' : int(form.hip_id.data),
                'record_id' : int(form.record_id.data),
                'user_type' : INVERSE_USER_TYPE_MAP[current_user.user_type]
        }
        response = requests.post('http://127.0.0.1:5000/get_data_request', json = data)
        return "Data : " + response.text
    else:
        return render_template('data_request.html', title = 'Consent', form = form)

@app.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', title = 'Home')
    else:
        return redirect(url_for('login'))

@app.route('/consent_listener', methods = ['POST'])
def consent_listener():
    content = request.get_json()
    consent = Consent.query.filter_by(id = content['consent_id']).first()
    consent.accept = content['accept']
    db.session.commit()
    return make_response("Received consent status", 201)