from flask import render_template, url_for, flash, redirect, request, make_response, jsonify
from hip.models import UserType, PurposeType, Record
from hip import app, db, bcrypt
import requests
import json

PURPOSE_MAP = {"Diagnosis" : PurposeType.DIAGNOSIS, "Prescription" : PurposeType.PRESCRIPTION}
USER_TYPE_MAP = {"Doctor" : UserType.DOCTOR, "Nurse" : UserType.NURSE, "Receptionist" : UserType.RECEPTIONIST, "Pharmacist" : UserType.PHARMACIST}

@app.route('/get_data_request', methods = ['POST'])
def get_data():
    content = request.get_json()
    record = Record.query.filter_by(id = content['record_id']).first()
    data = {
        'id' : record.id,
        'data' : record.data
    }
    return make_response(json.dumps(data), 201)

# @app.route('/consent_listener', methods = ['POST'])
# def consent_listener():
#     content = request.get_json()
#     consent = Consent.query.filter_by(id = content['consent_id']).first()
#     consent.accept = content['accept']
#     db.session.commit()
#     return make_response("Received consent status", 201)