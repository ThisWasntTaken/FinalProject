from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, BooleanField, RadioField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from hiu.models import User, Patient, PurposeType, UserType

USER_TYPE = ["Doctor", "Nurse", "Receptionist", "Pharmacist"]
PURPOSE = ["Diagnosis", "Prescription"]

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

        user = User.query.filter_by(digi_doctor_id = digi_doctor_id.data).first()
        if user:
            raise ValidationError('A user with that DigiDoctor ID already exists!')

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

class ConsentForm(FlaskForm):
    health_id = IntegerField('Health ID', validators = [DataRequired()])
    hip_id = IntegerField('HIP ID', validators = [DataRequired()])
    record_id = IntegerField('Record ID', validators = [DataRequired()])
    purpose = SelectField('Purpose', choices = [(i, i) for i in PURPOSE], validators = [DataRequired()])
    time_from = DateField('Time when consent is given', format = '%Y-%m-%d', validators = [DataRequired()])
    time_to = DateField('Time till consent is active', format = '%Y-%m-%d', validators = [DataRequired()])
    submit = SubmitField('Submit Consent Request')

    def validate_health_id(self, health_id):
        patient = Patient.query.filter_by(health_id = health_id.data).first()
        if not patient:
            raise ValidationError('A patient with that Health ID does not exist!')

    def validate_time_to(self, time_to):
        if self.time_from.data > time_to.data:
            raise ValidationError('Enter valid dates.')