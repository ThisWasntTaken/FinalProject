from hiu import db, login_manager
from flask_login import UserMixin
from utils import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    public_key = db.Column(db.BLOB, unique = True, nullable = False)

    def __repr__(self):
        return f"Patient({self.health_id}, {self.name}, {self.email})"

class Consent(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    derived_from = db.Column(db.Integer, db.ForeignKey('consent.id'), nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable = False)
    hip_id = db.Column(db.Integer, nullable = False)
    artefact = db.Column(db.BLOB, nullable = True)
    signature = db.Column(db.BLOB, nullable = True)
    status = db.Column(db.Enum(StatusType), nullable = False)

    def __repr__(self):
        return f"Consent(ID = {self.id}, Patient ID = {self.patient_id}, HIP ID = {self.hip_id})"

    def __str__(self):
        return f"Consent(ID = {self.id}, Patient ID = {self.patient_id}, HIP ID = {self.hip_id})"