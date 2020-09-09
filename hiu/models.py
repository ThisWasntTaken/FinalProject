from hiu import db, login_manager
import enum
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class UserType(enum.Enum):
    DOCTOR = "Doctor"
    NURSE = "Nurse"
    RECEPTIONIST = "Receptionist"
    PHARMACIST = "Pharmacist"

class PurposeType(enum.Enum):
    DIAGNOSIS = "Diagnosis"
    PRESCRIPTION = "Prescription"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    digi_doctor_id = db.Column(db.String(20), unique = True, nullable = True)
    name = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    phone = db.Column(db.String(10), unique = False, nullable = False)
    user_type = db.Column(db.Enum(UserType), nullable = False)
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"User({self.name}, {self.email}, {self.user_type})"

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    health_id = db.Column(db.String(20), nullable = True, unique = True)
    name = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)

    def __repr__(self):
        return f"Patient({self.health_id}, {self.name}, {self.email})"

class Consent(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable = False)
    hip_id = db.Column(db.Integer, nullable = False)
    record_id = db.Column(db.Integer, nullable = False)
    purpose = db.Column(db.Enum(PurposeType), nullable = False)
    time_from = db.Column(db.DateTime, nullable = False)
    time_to = db.Column(db.DateTime, nullable = False)
    accept = db.Column(db.Boolean, default = False, nullable = False)

    def __repr__(self):
        return f"Consent({self.id}, {self.patient_id}, {self.record_id}, {self.accept})"

    def __str__(self):
        return f"Record {self.record_id} of HIP {self.hip_id} for {self.purpose} from {self.time_from.strftime('%Y-%m-%d')} to {self.time_to.strftime('%Y-%m-%d')}"

# db.create_all()