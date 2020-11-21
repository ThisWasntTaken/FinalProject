from flask import request, make_response, jsonify
from gateway.models import Hiu, Hip
from gateway import app, db
import requests

@app.route('/get_consent_request', methods = ['POST'])
def get_consent_request():
    content = request.get_json()
    print(content)
    hiu = Hiu.query.filter_by(id = content['hiu_id']).first()
    hip = Hip.query.filter_by(id = content['hip_id']).first()
    content['hiu_name'] = hiu.name
    content['hip_name'] = hip.name
    response = requests.post('http://127.0.0.1:5001/get_consent_request', json = content)
    return make_response(response.text, response.status_code)

@app.route('/consent_listener', methods = ['POST'])
def consent_listener():
    content = request.get_json()
    hiu = Hiu.query.filter_by(id = content['hiu_id']).first()
    if not hiu:
        return make_response("No HIU with that ID", 404)
    response = requests.post(hiu.url + '/consent_listener', json = content)
    return make_response(response.text, response.status_code)

@app.route('/get_data_request', methods = ['POST'])
def get_data_request():
    content = request.get_json()
    hip = Hip.query.filter_by(id = content['hip_id']).first()
    if not hip:
        return make_response("No HIP with that ID", 404)
    response = requests.post(hip.url + '/get_data_request', json = content)
    return make_response(response.text, response.status_code)