from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, BooleanField, RadioField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, optional
from hiup.models import User, Patient, Consent
from hiup import bcrypt
from utils import *

USER_TYPE = USER_TYPE_MAP.keys()
PURPOSE = PURPOSE_MAP.keys()

class RegistrationForm(FlaskForm):
    user_type = SelectField('Type of User', choices = [(i, i) for i in USER_TYPE], validators = [DataRequired()])
    digi_doctor_id = StringField('DigiDoctor ID')
    name = StringField('Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    phone = StringField('Phone Number', validators = [DataRequired(), Length(min = 10, max = 10)])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_digi_doctor_id(self, digi_doctor_id):
        if self.user_type.data != "Doctor" and digi_doctor_id.data != "":
            raise ValidationError('Only doctors can enter a DigiDoctor ID!')
        
        if self.user_type.data == "Doctor" and digi_doctor_id.data == "":
            raise ValidationError('Doctors need to enter their DigiDoctor ID!')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('A user with that Email already exists!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if not user:
            raise ValidationError('A user with that email does not exist!')

    def validate_password(self, password):
        user = User.query.filter_by(email = self.email.data).first()
        if not (user and bcrypt.check_password_hash(user.password, password.data)):
            raise ValidationError('Wrong password')

class ConsentForm(FlaskForm):
    health_id = StringField('Health ID', validators = [DataRequired()])
    hip_id = IntegerField('HIP ID', validators = [DataRequired()])
    encounter_id = IntegerField('Encounter ID', validators = [optional()])
    record_id = IntegerField('Record ID', validators = [optional()])
    purpose = SelectField('Purpose', choices = [(i, i) for i in PURPOSE], validators = [DataRequired()])
    time_from = DateField('Time when consent is given', format = '%Y-%m-%d', validators = [DataRequired()])
    time_to = DateField('Time till consent is active', format = '%Y-%m-%d', validators = [DataRequired()])
    submit = SubmitField('Submit Consent Request')

    def validate(self, extra_validators=None):
        if super().validate(extra_validators):

            if not (self.encounter_id.data or self.record_id.data):
                self.encounter_id.errors.append('At least one of Encounter ID and Record ID must have a value.')
                self.record_id.errors.append('At least one of Encounter ID and Record ID must have a value.')
                return False
            else:
                return True

        return False

    def validate_health_id(self, health_id):
        patient = Patient.query.filter_by(health_id = health_id.data).first()
        if not patient:
            raise ValidationError('A patient with that Health ID does not exist!')

    def validate_time_to(self, time_to):
        if self.time_from.data > time_to.data:
            raise ValidationError('Enter valid dates.')

class DataRequestForm(FlaskForm):
    purpose = SelectField('Purpose', choices = [(i, i) for i in PURPOSE], validators = [DataRequired()])
    consent_id = SelectField('Consent', validators = [DataRequired()])
    cache = BooleanField('Cache this data?')
    submit = SubmitField('Submit Data Request')

class CreateTeamForm(FlaskForm):
    consent_id = IntegerField('Consent ID', validators = [DataRequired()])
    id_1 = IntegerField('ID of member', validators = [DataRequired()])
    id_2 = IntegerField('ID of member', validators = [DataRequired()])
    submit = SubmitField('Create Team')

    def validate_consent_id(self, consent_id):
        consent = Consent.query.filter_by(id = consent_id.data).first()
        if not consent:
            raise ValidationError('A consent with that ID does not exist!')

    def validate_id_1(self, id_1):
        user = User.query.filter_by(id = id_1.data).first()
        if not user:
            raise ValidationError('A user with that ID does not exist!')

    def validate_id_2(self, id_2):
        user = User.query.filter_by(id = id_2.data).first()
        if not user:
            raise ValidationError('A user with that ID does not exist!')