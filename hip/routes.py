from flask import render_template, url_for, flash, redirect, request, make_response, jsonify
from hip.models import UserType, PurposeType
from hip.forms import RegistrationForm, LoginForm, ConsentForm
from hip import app, db, bcrypt
import requests

PURPOSE_MAP = {"Diagnosis" : PurposeType.DIAGNOSIS, "Prescription" : PurposeType.PRESCRIPTION}
USER_TYPE_MAP = {"Doctor" : UserType.DOCTOR, "Nurse" : UserType.NURSE, "Receptionist" : UserType.RECEPTIONIST, "Pharmacist" : UserType.PHARMACIST}

@app.route('/get_data', methods = ['POST'])
def get_data():
    # content = request.get_json()
    d = {'id' : 1}
    print(jsonify(d))

# @app.route('/consent_listener', methods = ['POST'])
# def consent_listener():
#     content = request.get_json()
#     consent = Consent.query.filter_by(id = content['consent_id']).first()
#     consent.accept = content['accept']
#     db.session.commit()
#     return make_response("Received consent status", 201)