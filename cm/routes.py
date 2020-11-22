"""
API documentation for Consent Manager.
"""

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

@app.route('/consent_request', methods = ['POST'])
def get_consent_request():
    """
    .. http:post:: /consent_request/

        Add a consent request for a user (patient).

        **Example request**:

        .. sourcecode:: http

            POST /get_consent_request/ HTTP/1.1
            Host: http://127.0.0.1:5001/
            Content-Type: application/json

            {
                "request_id": 1,
                "health_id": "1",
                "hiu_id": 1,
                "requester_name": "Doctor1",
                "hip_id": 2,
                "purpose": "Diagnosis",
                "time_from": "2020-11-21",
                "time_to": "2020-11-23",
                "encounter_id": 1,
                "hiu_name": "Hiu1",
                "hip_name": "Hip2"
            }
        
        :<json int request_id: ID of the consent request at the HIU.
        :<json string health_id: Health ID of the user (patient).
        :<json int hiu_id: ID of the HIU.
        :<json string requester_name: Name of the user requesting the consent.
        :<json int hip_id: ID of the HIP.
        :<json string purpose: Purpose of the consent request.
        :<json string time_from: Date from which the consent is valid.
        :<json string time_to: Date till which the consent is valid.
        :<json int encounter_id: **optional** ID of the encounter at the HIP.
        :<json int record_id: **optional** ID of the record at the HIP.
        :<json int hiu_name: Name of the HIU.
        :<json int hip_name: Name of the HIP.

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 Received Request
        
        :statuscode 201: Received Request
        :statuscode 400: User not found
    """
    content = request.get_json()
    time_from = datetime.strptime(content['time_from'], '%Y-%m-%d').date()
    time_to = datetime.strptime(content['time_to'], '%Y-%m-%d').date()
    user = User.query.filter_by(health_id = content['health_id']).first()
    if not user:
        return make_response("", 400)
    
    r = Consent_Request(user_id = user.id,
                        request_id = content['request_id'],
                        hiu_id = content['hiu_id'],
                        hiu_name = content['hiu_name'],
                        requester_name = content['requester_name'],
                        hip_id = content['hip_id'],
                        hip_name = content['hip_name'],
                        encounter_id = content['encounter_id'] if 'encounter_id' in content.keys() else None,
                        record_id = content['record_id'] if 'record_id' in content.keys() else None,
                        purpose = PURPOSE_MAP[content['purpose']],
                        time_from = time_from,
                        time_to = time_to,
                        status = StatusType.ACTIVE
                    )
    db.session.add(r)
    db.session.commit()
    return make_response("", 201)

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
        return render_template('home.html', title = 'Home', requests = requests, inverse_serialization_helper = INVERSE_SERIALIZATION_HELPER)
    else:
        return redirect(url_for('login'))

@app.route('/view_approvals')
@login_required
def view_approvals():
    if current_user.is_authenticated:
        requests = Consent_Request.query.filter_by(user_id = current_user.id, status = StatusType.ACCEPTED).filter(Consent_Request.time_to >= datetime.now().date())
        return render_template('view_approvals.html', title = 'View Approvals', requests = requests, inverse_serialization_helper = INVERSE_SERIALIZATION_HELPER)
    else:
        return redirect(url_for('login'))

@app.route("/request/<int:request_id>/accept", methods = ['GET', 'POST'])
def accept_request(request_id):
    form = PrivateKeyForm()
    if request.method == 'POST' and form.validate_on_submit():
        file_path = os.path.join(app.instance_path, '..', form.file.data.filename)
        with open(file_path,'rb') as f:
            private_key = RSA.import_key(f.read())
        
        req = Consent_Request.query.filter_by(id = request_id).first()
        artefact = {
            "hiu_id" : req.hiu_id,
            "hip_id" : req.hip_id,
            "purpose" : INVERSE_SERIALIZATION_HELPER[req.purpose],
            "time_from" : str(req.time_from.date()),
            "time_to" : str(req.time_to.date())
        }
        if req.encounter_id:
            artefact["encounter_id"] = req.encounter_id
        if req.record_id:
            artefact["record_id"] = req.record_id
        
        artefact = json.dumps(artefact)
        h = SHA256.new(artefact.encode('utf-8'))
        signature = base64.b64encode(pss.new(private_key).sign(h)).decode('utf-8')
        data = {'consent_id' : req.request_id, 'hiu_id' : req.hiu_id, 'artefact' : artefact, 'signature' : signature, 'accept' : True}
        response = requests.post('http://127.0.0.1:5000/consent_listener', json = data)
        if response.status_code == 201:
            flash(f'Your consent has been sent.', 'success')
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
    if response.status_code == 201:
        flash(f'Your consent denial has been sent.', 'success')
        if req.status == StatusType.ACCEPTED:
            req.status = StatusType.REVOKED
            db.session.commit()
            return redirect(url_for('view_approvals'))
        elif req.status == StatusType.ACTIVE:
            req.status = StatusType.DENIED
            db.session.commit()
            return redirect(url_for('home'))
    else:
        flash(f'Your consent denial was not sent. Please try again.', 'danger')
        return redirect(url_for('view_approvals'))