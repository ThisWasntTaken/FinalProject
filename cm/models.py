"""
Database models of Consent Manager.
"""

from cm import db, login_manager
from flask_login import UserMixin
from utils import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
    User (Patient) details and login information.

    :param int id: **primary key**
    :param str health_id: Unique health id of the user
    :param str name: Name of the user
    :param str email: Email of the user
    :param str phone: Phone number of the user
    :param str password: Encrypted password of the user
    """
    id = db.Column(db.Integer, primary_key = True)
    health_id = db.Column(db.String(20), unique = True)
    name = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    phone = db.Column(db.String(10), unique = False, nullable = False)
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        """
        Return the string representation of the user.
        """
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}', '{self.phone}')"

class Consent_Request(db.Model):
    """
    Details of a Consent Request.

    :param int id: **primary key**
    :param int request_id: ID of the consent request at the HIU
    :param int user_id: **foreign key to User** ID of the user (patient)
    :param int hiu_id: ID of the HIU
    :param str hiu_name: Name of the HIU
    :param str requester_name: Name of the user requesting for consent
    :param int hip_id: ID of the HIP
    :param str hip_name: Name of the HIP
    :param int encounter_id: **nullable** ID of the Encounter
    :param int record_id: **nullable** ID of the Record
    :param Enum(utils.PurposeType) purpose: Purpose of the request
    :param DateTime time_from: Time from which the consent is valid
    :param DateTime time_to: Time till which the consent is valid
    :param Enum(utils.StatusType) status: Status of the request
    """
    id = db.Column(db.Integer, primary_key = True)
    request_id = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    hiu_id = db.Column(db.Integer, nullable = False)
    hiu_name = db.Column(db.String(40), nullable = False)
    requester_name = db.Column(db.String(40), nullable = False)
    hip_id = db.Column(db.Integer, nullable = False)
    hip_name = db.Column(db.String(40), nullable = False)
    encounter_id = db.Column(db.Integer, nullable = True)
    record_id = db.Column(db.Integer, nullable = True)
    purpose = db.Column(db.Enum(PurposeType), nullable = False)
    time_from = db.Column(db.DateTime, nullable = False)
    time_to = db.Column(db.DateTime, nullable = False)
    status = db.Column(db.Enum(StatusType), nullable = False)