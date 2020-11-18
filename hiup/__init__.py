from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from argparse import ArgumentParser

def create_app(hiu_id, hip_id):
    app = Flask(__name__)
    app.config['HIU_ID'] = hiu_id
    app.config['HIP_ID'] = hip_id
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site' + str(hiu_id) + "_" + str(hip_id) + '.db'
    app.config['SECRET_KEY'] = 'c7e0792f8c63365236839f7205de037e'
    app.config['SESSION_COOKIE_NAME'] = "cookie_" + str(hiu_id) + "_" + str(hip_id)
    return app

parser = ArgumentParser()
parser.add_argument('-hiu_id')
parser.add_argument('-hip_id')
args = parser.parse_args()
hiu_id = args.hiu_id
hip_id = args.hip_id
app = create_app(hiu_id, hip_id)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from hiup import routes