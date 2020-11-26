from flask import request, make_response, jsonify
from gateway.models import Hiu, Hip
from gateway import app, db
import requests

@app.route('/consent_request', methods = ['POST'])
def consent_request():
    """
    .. http:post:: /consent_request/

        Pass a consent request to the Consent Manager.

        **Example request**:

        .. sourcecode:: http

            POST /consent_request/ HTTP/1.1
            Host: http://127.0.0.1:5000/
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

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 Received Request
            Content-Type: text/plain
        
        :statuscode 201: Received Request
        :statuscode 400: User not found
        :statuscode 400: HIU not found
        :statuscode 400: HIP not found
    """
    content = request.get_json()
    hiu = Hiu.query.filter_by(id = content['hiu_id']).first()
    if not hiu:
        return make_response("HIU not found", 400)
    hip = Hip.query.filter_by(id = content['hip_id']).first()
    if not hip:
        return make_response("HIP not found", 400)
    content['hiu_name'] = hiu.name
    content['hip_name'] = hip.name
    response = requests.post('http://127.0.0.1:5001/consent_request', json = content)
    return make_response(response.text, response.status_code)

@app.route('/consent_listener', methods = ['POST'])
def consent_listener():
    """
    .. http:post:: /consent_listener/

        Pass a consent status and object to a HIU.

        **Example request**:

        .. sourcecode:: http

            POST /consent_listener/ HTTP/1.1
            Host: http://127.0.0.1:5000/
            Content-Type: application/json

            {
                "consent_id": 1,
                "hiu_id": 1,
                "artefact":
                    {
                        "hiu_id": 1,
                        "hip_id": 1,
                        "purpose": "Diagnosis",
                        "time_from": "2020-11-21",
                        "time_to": "2020-11-23",
                        "encounter_id": 1
                    },
                "signature": ".....",
                "accept": true
            }
        
        :<json int consent_id: ID of the consent request at the HIU.
        :<json int hiu_id: ID of the HIU.
        :<json json artefact: Consent Artefact.
        :<json string signature: Digital signature of the artefact.
        :<json bool accept: Status of the consent request.

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 Received Request
            Content-Type: text/plain
        
        :statuscode 201: Received Request
        :statuscode 400: HIU not found
        :statuscode 401: Invalid Signature
    """
    content = request.get_json()
    hiu = Hiu.query.filter_by(id = content['hiu_id']).first()
    if not hiu:
        return make_response("HIU not found", 400)
    response = requests.post(hiu.url + '/consent_listener', json = content)
    return make_response(response.text, response.status_code)

@app.route('/get_data_request', methods = ['POST'])
def get_data_request():
    """
    .. http:post:: /get_data_request/

        Pass a data request to a HIP.

        **Example request**:

        .. sourcecode:: http

            POST /get_data_request/ HTTP/1.1
            Host: http://127.0.0.1:5000/
            Content-Type: application/json

            {
                "artefact": 
                    {
                        "hiu_id": 1,
                        "hip_id": 2,
                        "purpose": "Diagnosis",
                        "time_from": "2020-11-21",
                        "time_to": "2020-11-23",
                        "encounter_id": 1
                    },
                "signature": ".....",
                "health_id": "1",
                "hip_id": 2,
                "activity": "Diagnosis1",
                "hiu_id": 1,
                "user_id": 1,
                "user_type": "Doctor"
            }
        
        :<json json artefact: Consent Artefact.
        :<json string signature: Digital signature of the artefact.
        :<json string health_id: Health ID of the user (patient).
        :<json int hip_id: ID of the HIP.
        :<json string activity: Activity that requires data.
        :<json int hiu_id: ID of the HIU.
        :<json int user_id: ID of the user who is requesting data.
        :<json string user_type: UserType of the user who is requesting data.

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 Received Request
            Content-Type: application/json

            {
                "1": 
                [
                    "Patient1's Encounter 1, Record 1 Prescription at Hiu2",
                    "Prescription"
                ],
                "2": 
                [
                    "Patient1's Encounter 1, Record 2 MRI at Hiu2",
                    "MRI"
                ],
                "3": 
                [
                    "Patient1's Encounter 1, Record 3 Registration at Hiu2",
                    "Registration"
                ]
            }
        
        :statuscode 201: Received Request
        :statuscode 400: HIP not found
        :statuscode 401: Invalid Signature
        :statuscode 404: Record not found
        :statuscode 404: Encounter not found
    """
    content = request.get_json()
    hip = Hip.query.filter_by(id = content['hip_id']).first()
    if not hip:
        return make_response("HIP not found", 400)
    response = requests.post(hip.url + '/get_data_request', json = content)
    return make_response(response.text, response.status_code)