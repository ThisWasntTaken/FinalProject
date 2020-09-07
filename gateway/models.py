from gateway import db

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    digi_doctor_id = db.Column(db.String(20), unique = True, nullable = False)
    name = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    phone = db.Column(db.String(10), unique = True, nullable = False)

class Hiu(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), unique = True, nullable = False)
    url = db.Column(db.String(100), unique = True, nullable = False)

class Hip(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), unique = True, nullable = False)
    url = db.Column(db.String(100), unique = True, nullable = False)