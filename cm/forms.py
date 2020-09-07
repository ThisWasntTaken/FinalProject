from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from cm.models import User

class RegistrationForm(FlaskForm):
    health_id = StringField('Health ID', validators = [DataRequired()])
    name = StringField('Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    phone = StringField('Phone Number', validators = [DataRequired(), Length(min = 10, max = 10)])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_health_id(self, health_id):
        user = User.query.filter_by(health_id = health_id.data).first()
        if user:
            raise ValidationError('A user with that Health ID already exists!')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('A user with that Email already exists!')

class LoginForm(FlaskForm):
    health_id = StringField('Health ID', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_health_id(self, health_id):
        user = User.query.filter_by(health_id = health_id.data).first()
        if not user:
            raise ValidationError('A user with that Health ID does not exist!')