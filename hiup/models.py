from hiup import db, login_manager
from flask_login import UserMixin
from utils import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
    User (Patient) details and login information.

    :param int id: **primary key**
    :param str digi_doctor_id: **nullable** Unique digi doctor id of the user
    :param str name: Name of the user
    :param str email: Email of the user
    :param str phone: Phone number of the user
    :param Enum(utils.UserType) user_type: Type of the user
    :param str password: Encrypted password of the user
    """
    id = db.Column(db.Integer, primary_key = True)
    digi_doctor_id = db.Column(db.String(20), unique = True, nullable = True)
    name = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    phone = db.Column(db.String(10), unique = False, nullable = False)
    user_type = db.Column(db.Enum(UserType), nullable = False)
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        """
        Return the string representation of the user.
        """
        return f"User({self.name}, {self.email}, {self.user_type})"

class Patient(db.Model):
    """
    User (Patient) details and login information.

    :param int id: **primary key**
    :param str health_id: Unique health id of the user
    :param str name: Name of the user
    :param str email: Email of the user
    :param BLOB public_key: Public key of the user
    """
    id = db.Column(db.Integer, primary_key = True)
    health_id = db.Column(db.String(20), nullable = False, unique = True)
    name = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    public_key = db.Column(db.BLOB, unique = True, nullable = False)

    def __repr__(self):
        """
        Return the string representation of the patient.
        """
        return f"Patient({self.health_id}, {self.name}, {self.email})"

class Consent(db.Model):
    """
    Consents asked for, accepted, revoked, or denied.

    :param int id: **primary key**
    :param int user_id: **foreign key to User** ID of the user to whom consent was given
    :param int patient_id: **foreign key to Patient** ID of the patient
    :param int hip_id: ID of the HIP
    :param BLOB artefact: Consent artefact
    :param BLOB signature: Digital signature of the consent artefact
    :param Enum(utils.StatusType) status: status of consent
    :param int encounter_id: **nullable, foreign key to Encounter** ID of cached encounter
    :param int record_id: **nullable, foreign key to Record** ID of cached record
    """
    id = db.Column(db.Integer, primary_key = True)
    # derived_from = db.Column(db.Integer, db.ForeignKey('consent.id'), nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable = False)
    hip_id = db.Column(db.Integer, nullable = False)
    artefact = db.Column(db.BLOB, nullable = True)
    signature = db.Column(db.BLOB, nullable = True)
    state = db.Column(db.Enum(State), nullable = False)
    status = db.Column(db.Enum(StatusType), nullable = False)
    encounter_id = db.Column(db.Integer, db.ForeignKey('encounter.id'), nullable = True)
    record_id = db.Column(db.Integer, db.ForeignKey('record.id'), nullable = True)

    def __repr__(self):
        return f"Consent(ID = {self.id}, User ID = {self.user_id}, Patient ID = {self.patient_id}, HIP ID = {self.hip_id})"

    def __str__(self):
        return f"Consent(ID = {self.id}, User ID = {self.user_id}, Patient ID = {self.patient_id}, HIP ID = {self.hip_id})"

class Encounter(db.Model):
    """
    Encounter.

    :param int id: **primary key**
    :param int patient_id: **foreign key to Patient** ID of the patient
    """
    id = db.Column(db.Integer, primary_key = True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable = False)

class Record(db.Model):
    """
    A data record.

    :param int id: **primary key**
    :param int encounter_id: **foreign key to Patient** ID of the patient
    :param int patient_id: **foreign key to Patient** ID of the patient
    :param str data: data
    :param Enum(utils.RecordType): Type of data
    """
    id = db.Column(db.Integer, primary_key = True)
    encounter_id = db.Column(db.Integer, db.ForeignKey('encounter.id'), nullable = True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable = False)
    data = db.Column(db.String(100), nullable = False)
    record_type = db.Column(db.Enum(RecordType), nullable = False)
    
    def __repr__(self):
        return f"Record({self.id}, {self.patient_id}, {self.data}, {self.record_type})"

class Request_Log(db.Model):
    """
    Log of data request.

    :param int id: **primary key**
    :param int consent_id: **foreign key to Consent** ID of the consent used for data request
    :param str activity: Activity that requires data
    :param DateTime time: Time of data request
    """
    id = db.Column(db.Integer, primary_key = True)
    consent_id = db.Column(db.Integer, db.ForeignKey('consent.id'), nullable = False)
    #TODO I cannot find a way to enumerate activity types using db.Enum. I have settled on using string.
    activity = db.Column(db.String(100), nullable = False)
    time = db.Column(db.DateTime, nullable = False)

class Access_Log(db.Model):
    """
    Log of data access.

    :param int id: **primary key**
    :param int hiu_id: ID of the HIU
    :param int user_id: **foreign key to User** ID of the user who requested data
    :param BLOB artefact: Consent artefact used to access data
    :param BLOB signature: Digital signature of the consent artefact for non-repudiability
    :param str activity: Activity that requires data
    :param DateTime time: Time of data access
    """
    id = db.Column(db.Integer, primary_key = True)
    hiu_id = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, nullable = False)
    artefact = db.Column(db.BLOB, nullable = False)
    signature = db.Column(db.BLOB, nullable = False)
    #TODO I cannot find a way to enumerate activity types using db.Enum. I have settled on using string.
    activity = db.Column(db.String(100), nullable = False)
    time = db.Column(db.DateTime, nullable = False)