from flask import render_template, url_for, flash, redirect, request, make_response, jsonify
from cm.models import User, Consent_Request
from cm.forms import RegistrationForm, LoginForm, PrivateKeyForm
from cm import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import requests
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
import json
import base64
import os
from utils import *

@app.route('/get_consent_request', methods = ['POST'])
def get_consent_request():
    content = request.get_json()
    time_from = datetime.strptime(content['time_from'], '%Y-%m-%d').date()
    time_to = datetime.strptime(content['time_to'], '%Y-%m-%d').date()
    user = User.query.filter_by(health_id = content['health_id']).first()
    if not user:
        return make_response("No such user", 400)
    
    r = Consent_Request(user_id = user.id,
                        request_id = content['request_id'],
                        hiu_id = content['hiu_id'],
                        hiu_name = content['hiu_name'],
                        requester_name = content['requester_name'],
                        hip_id = content['hip_id'],
                        hip_name = content['hip_name'],
                        encounter_id = content['encounter_id'],
                        record_id = content['record_id'],
                        purpose = PURPOSE_MAP[content['purpose']],
                        time_from = time_from,
                        time_to = time_to,
                        status = StatusType.ACTIVE
                    )
    db.session.add(r)
    db.session.commit()
    return make_response("Received request", 201)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(health_id = form.health_id.data).first()
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
        user = User(health_id = form.health_id.data, name = form.name.data, email = form.email.data, phone = form.phone.data, password = password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('register.html', title = 'Register', form = form)

@app.route('/')
@app.route('/home')
@login_required
def home():
    if current_user.is_authenticated:
        requests = Consent_Request.query.filter_by(user_id = current_user.id, status = StatusType.ACTIVE)
        return render_template('home.html', title = 'Home', requests = requests, inverse_purpose_map = INVERSE_PURPOSE_MAP)
    else:
        return redirect(url_for('login'))

@app.route('/view_approvals')
@login_required
def view_approvals():
    if current_user.is_authenticated:
        requests = Consent_Request.query.filter_by(user_id = current_user.id, status = StatusType.ACCEPTED).filter(Consent_Request.time_to >= datetime.now().date())
        return render_template('view_approvals.html', title = 'View Approvals', requests = requests, inverse_purpose_map = INVERSE_PURPOSE_MAP)
    else:
        return redirect(url_for('login'))

@app.route("/request/<int:request_id>/accept", methods = ['GET', 'POST'])
def accept_request(request_id):
    form = PrivateKeyForm()
    if request.method == 'POST' and form.validate_on_submit():
        file_path = os.path.join(app.instance_path, '..', form.file.data.filename)
        print(file_path)
        with open(file_path,'rb') as f:
            private_key = RSA.import_key(f.read())
        
        req = Consent_Request.query.filter_by(id = request_id).first()
        artefact = json.dumps({
            "encounter_id" : req.encounter_id,
            "record_id" : req.record_id,
            "hip_id" : req.hip_id,
            "purpose" : INVERSE_PURPOSE_MAP[req.purpose],
            "time_from" : str(req.time_from),
            "time_to" : str(req.time_to)
        })
        h = SHA256.new(artefact.encode('utf-8'))
        signature = base64.b64encode(pss.new(private_key).sign(h)).decode('utf-8')
        data = {'consent_id' : req.request_id, 'hiu_id' : req.hiu_id, 'artefact' : artefact, 'signature' : signature, 'accept' : True}
        response = requests.post('http://127.0.0.1:5000/consent_listener', json = data)
        flash(f'Your consent has been sent.', 'success')
        if response.status_code == 201:
            req.status = StatusType.ACCEPTED
            db.session.commit()
        elif response.status_code == 401:
            flash(f'Invalid Signature. Your consent was not accepted.', 'danger')
        return redirect(url_for('home'))
    else:
        return render_template('private_key_upload.html', title = 'Generate Consent Artefact', form=form)

@app.route("/request/<int:request_id>/deny")
def deny_request(request_id):
    req = Consent_Request.query.filter_by(id = request_id).first()
    data = {'consent_id' : req.request_id, 'hiu_id' : req.hiu_id, 'accept' : False}
    response = requests.post('http://127.0.0.1:5000/consent_listener', json = data)
    flash(f'Your consent denial has been sent.', 'success')
    req.status = StatusType.REVOKED
    db.session.commit()
    return redirect(url_for('home'))