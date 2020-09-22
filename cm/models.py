from cm import db, login_manager
import enum
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class PurposeType(enum.Enum):
    DIAGNOSIS = "diagnosis"
    PRESCRIPTION = "prescription"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    health_id = db.Column(db.String(20), unique = True)
    name = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    phone = db.Column(db.String(10), unique = False, nullable = False)
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}', '{self.phone}')"

class Consent_Request(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    request_id = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    hiu_id = db.Column(db.Integer, nullable = False)
    hiu_name = db.Column(db.String(40), nullable = False)
    requester_name = db.Column(db.String(40), nullable = False)
    hip_id = db.Column(db.Integer, nullable = False)
    hip_name = db.Column(db.String(40), nullable = False)
    record_id = db.Column(db.Integer, nullable = False)
    purpose = db.Column(db.Enum(PurposeType), nullable = False)
    time_from = db.Column(db.DateTime, nullable = False)
    time_to = db.Column(db.DateTime, nullable = False)
    accept = db.Column(db.Boolean, default = False, nullable = False)