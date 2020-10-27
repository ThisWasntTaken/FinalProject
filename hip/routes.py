from flask import render_template, url_for, flash, redirect, request, make_response, jsonify
from hip.models import Record, Patient
from hip import app, db, bcrypt
import requests
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
import json
import base64
from utils import *

@app.route('/get_data_request', methods = ['POST'])
def get_data():
    content = request.get_json()
    patient = Patient.query.filter_by(health_id = content['health_id']).first()
    signature = base64.b64decode(content['signature'].encode('utf-8'))
    artefact = content['artefact']
    h = SHA256.new(artefact.encode('utf-8'))
    verifier = pss.new(RSA.import_key(patient.public_key))
    try:
        verifier.verify(h, signature)
        artefact = json.loads(artefact)
        record = Record.query.filter_by(id = artefact['record_id']).first()
        if not record:
            return make_response("Record not found", 404)
        data = {
            'id' : record.id,
            'data' : record.data
        }
        return make_response(json.dumps(data), 201)
    except:
        return make_response("Invalid Signature", 401)