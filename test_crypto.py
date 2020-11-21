from hiup.models import Encounter
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
import json
import base64
from utils import RecordType

artefact = json.dumps({"1":1, "2":2})

# private_key = RSA.generate(2048)
# with open('./private_key.pem','wb') as f:
#     f.write(private_key.exportKey('PEM'))

with open('./private_key.pem','rb') as f:
    private_key = RSA.import_key(f.read())

h = SHA256.new(artefact.encode('utf-8'))
signature = pss.new(private_key).sign(h)
signature = base64.b64encode(signature).decode('utf-8')
j = json.dumps({'artefact' : artefact, 'signature' : signature})

# public_key = private_key.publickey()
# with open('./public_key.pem','wb') as f:
#     f.write(public_key.exportKey('PEM'))
#     from hiup import db
#     from hiup.models import Patient
#     patient = Patient(health_id = 1, name = "Patient1", email = "patient@patient.com", public_key = public_key.export_key())
#     db.session.add(patient)
#     db.session.commit()

# with open('./public_key.pem','rb') as f:
#     from hiup import db
#     from hiup.models import Patient, Record
#     public_key = RSA.import_key(f.read())
#     patient = Patient(health_id = 1, name = "Patient1", email = "patient1@patient.com", public_key = public_key.export_key())
#     db.session.add(patient)
#     db.session.commit()
#     encounter = Encounter(patient_id = 1)
#     db.session.add(encounter)
#     db.session.commit()
#     record = Record(encounter_id = 1, patient_id = 1, data = "Patient1's Encounter 1, Record 1 Prescription at Hiu1", record_type = RecordType.PRESCRIPTION)
#     db.session.add(record)
#     record = Record(encounter_id = 1, patient_id = 1, data = "Patient1's Encounter 1, Record 2 MRI at Hiu1", record_type = RecordType.MRI)
#     db.session.add(record)
#     record = Record(encounter_id = 1, patient_id = 1, data = "Patient1's Encounter 1, Record 3 Registration at Hiu1", record_type = RecordType.REGISTRATION)
#     db.session.add(record)
#     db.session.commit()
#     record = Record(patient_id = 1, data = "Patient1's Stand-alone, Record 4 Blood Test at Hiu1", record_type = RecordType.BLOOD_TEST)
#     db.session.add(record)
#     db.session.commit()

with open('./public_key.pem','rb') as f:
    public_key = RSA.import_key(f.read())

m = json.loads(j)
signature = base64.b64decode(m['signature'].encode('utf-8'))
h_p = SHA256.new(m['artefact'].encode('utf-8'))
verifier = pss.new(public_key)
try:
    verifier.verify(h_p, signature)
    print("The signature is authentic.")
except (ValueError, TypeError):
    print("The signature is not authentic.")