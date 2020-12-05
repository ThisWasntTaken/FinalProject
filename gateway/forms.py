from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddHIUForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    url = StringField('URL', validators = [DataRequired()])
    submit = SubmitField('Add HIU')

class AddHIPForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    url = StringField('URL', validators = [DataRequired()])
    submit = SubmitField('Add HIP')