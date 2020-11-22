from gateway import db

class Hiu(db.Model):
    """
    HIU details.

    :param int id: **primary key**
    :param str name: Name of the HIU
    :param str url: URL of the HIU
    """
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), unique = True, nullable = False)
    url = db.Column(db.String(100), unique = True, nullable = False)

class Hip(db.Model):
    """
    HIP details.

    :param int id: **primary key**
    :param str name: Name of the HIP
    :param str url: URL of the HIP
    """
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), unique = True, nullable = False)
    url = db.Column(db.String(100), unique = True, nullable = False)