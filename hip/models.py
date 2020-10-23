from hip import db, login_manager
from flask_login import UserMixin

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    health_id = db.Column(db.String(20), nullable = True, unique = True)
    name = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    public_key = db.Column(db.BLOB, unique = True, nullable = False)

    def __repr__(self):
        return f"Patient({self.health_id}, {self.name}, {self.email})"

class Record(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable = False)
    data = db.Column(db.String(100), nullable = False)

# class Consent(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
#     patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable = False)
#     record_id = db.Column(db.Integer, nullable = False)
#     purpose = db.Column(db.Enum(PurposeType), nullable = False)
#     time_from = db.Column(db.DateTime, nullable = False)
#     time_to = db.Column(db.DateTime, nullable = False)
#     accept = db.Column(db.Boolean, default = False, nullable = False)

#     def __repr__(self):
#         return f"Consent({self.patient_id}, {self.record_id}, {self.accept})"