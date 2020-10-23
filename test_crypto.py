from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
import json
import base64

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
#     from hiu import db
#     from hiu.models import Patient
#     patient = Patient(health_id = 1, name = "Jayanth Shreekumar", email = "jayanthshreekumar@gmail.com", public_key = public_key.export_key())
#     db.session.add(patient)
#     db.session.commit()

with open('./public_key.pem','rb') as f:
    from hip.models import Patient
    patient = Patient.query.filter_by(health_id = 1).first()
    public_key = RSA.import_key(patient.public_key)

m = json.loads(j)
signature = base64.b64decode(m['signature'].encode('utf-8'))
h_p = SHA256.new(m['artefact'].encode('utf-8'))
verifier = pss.new(public_key)
try:
    verifier.verify(h_p, signature)
    print("The signature is authentic.")
except (ValueError, TypeError):
    print("The signature is not authentic.")