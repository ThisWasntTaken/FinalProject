from flask import request, make_response, jsonify
from gateway.models import Hiu, Hip
from gateway import app, db
import requests

@app.route('/get_consent_request', methods = ['POST'])
def get_consent_request():
    content = request.get_json()
    hiu = Hiu.query.filter_by(id = content['hiu_id']).first()
    hip = Hip.query.filter_by(id = content['hip_id']).first()
    content['hiu_name'] = hiu.name
    content['hip_name'] = hip.name
    response = requests.post('http://127.0.0.1:5001/get_consent_request', json = content)
    return make_response("Received request", 201)

@app.route('/consent_listener', methods = ['POST'])
def consent_listener():
    content = request.get_json()
    hiu = Hiu.query.filter_by(id = content['hiu_id']).first()
    response = requests.post(hiu.url + '/consent_listener', json = content)
    return make_response("Recevied consent status", 201)