from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '36839f7205de037e0bec3fc6s6bd52ds'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SESSION_COOKIE_NAME'] = "gateway"
db = SQLAlchemy(app)

from gateway import routes