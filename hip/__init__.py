from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['HIP_ID'] = 1
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site' + str(app.config['HIP_ID']) + ".db"
app.config['SECRET_KEY'] = 'c7e0795facd1a95n36139f72z5de037e'
app.config['SESSION_COOKIE_NAME'] = "hip_" + str(app.config['HIP_ID'])
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from hip import routes