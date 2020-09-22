from flask import render_template, url_for, flash, redirect, request, make_response, jsonify
from cm.models import User, Consent_Request, PurposeType
from cm.forms import RegistrationForm, LoginForm
from cm import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import datetime
import requests

PURPOSE_MAP = {"Diagnosis" : PurposeType.DIAGNOSIS, "Prescription" : PurposeType.PRESCRIPTION}

@app.route('/get_consent_request', methods = ['POST'])
def get_consent_request():
    content = request.get_json()
    time_from = datetime.datetime.strptime(content['time_from'], '%Y-%m-%d').date()
    time_to = datetime.datetime.strptime(content['time_to'], '%Y-%m-%d').date()
    user = User.query.filter_by(health_id = content['health_id']).first()
    if not user:
        return make_response("No such user", 400)
    r = Consent_Request(user_id = user.id,
                        request_id = content['request_id'],
                        hiu_id = content['hiu_id'],
                        hiu_name = content['hiu_name'],
                        requester_name = content['requester_name'],
                        hip_id = content['hip_id'],
                        hip_name = content['hip_name'],
                        record_id = content['record_id'],
                        purpose = PURPOSE_MAP[content['purpose']],
                        time_from = time_from,
                        time_to = time_to,
                        accept = False
                    )
    db.session.add(r)
    db.session.commit()
    return make_response("Received request", 201)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(health_id = form.health_id.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    else:
        return render_template('login.html', title = 'Login', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(health_id = form.health_id.data, name = form.name.data, email = form.email.data, phone = form.phone.data, password = password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('register.html', title = 'Register', form = form)

@app.route('/')
@app.route('/home')
@login_required
def home():
    if current_user.is_authenticated:
        requests = Consent_Request.query.filter_by(user_id = current_user.id, accept = False)
        return render_template('home.html', title = 'Home', requests = requests)
    else:
        return redirect(url_for('login'))

@app.route('/view_approvals')
@login_required
def view_approvals():
    if current_user.is_authenticated:
        requests = Consent_Request.query.filter_by(user_id = current_user.id, accept = True)
        return render_template('view_approvals.html', title = 'View Approvals', requests = requests)
    else:
        return redirect(url_for('login'))

@app.route("/request/<int:request_id>/accept")
def accept_request(request_id):
    request = Consent_Request.query.filter_by(id = request_id).first()
    request.accept = True
    data = {'consent_id' : request.request_id, 'hiu_id' : request.hiu_id, 'accept' : True}
    response = requests.post('http://127.0.0.1:5000/consent_listener', json = data)
    flash(f'Your consent has been sent.', 'success')
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/request/<int:request_id>/deny")
def deny_request(request_id):
    request = Consent_Request.query.filter_by(id = request_id).first()
    data = {'consent_id' : request.request_id, 'hiu_id' : request.hiu_id, 'accept' : False}
    response = requests.post('http://127.0.0.1:5000/consent_listener', json = data)
    flash(f'Your consent denial has been sent.', 'success')
    db.session.delete(request)
    db.session.commit()
    return redirect(url_for('home'))