"""
CSCI991 Project Spring 2019, UOW
Team B
pt882@uowmail.edu.au
"""

import os
import json
import socket
import hashlib
import uuid
from threading import Thread
import datetime
import pickle

from flask import Flask
from flask import redirect, request, session, make_response, url_for
from flask import current_app, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message


################################################################################
# application and config:
# the static file: html JavaScript css images
app = Flask(__name__, static_url_path='',
            static_folder=os.environ.get('STATIC_FOLDER') or 'static')

# session
app.config['SESSION_TYPE'] = os.environ.get("SESSION_TYPE") or 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)

# database
app.config['SQLALCHEMY_DATABASE_URI'] = \
        os.environ.get('SQLALCHEMY_DATABASE_URI') \
        or 'sqlite:///./pi.sqlite3'

# email
app.config['MAIL_SERVER'] = 'smtp.live.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# !!! Do NOT put account and password in source !!!
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or ''
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or ''


################################################################################
# objects:
# database, Ref: pi.sqlite3.sql
db = SQLAlchemy(app)


class User(db.Model):
    # table: User
    email = db.Column(db.Text, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    activecode = db.Column(db.Text, nullable=False, unique=True)
    activity = db.Column(db.Integer, nullable=False)

    def __init__(self, email, password, activecode, activity):
        self.email = email
        self.password = password
        self.activecode = activecode
        self.activity = activity

    def __repr__(self):
        return '<User %>' % self.email


# email:
mail = Mail(app)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, body):
    # To be a robust system, there should be one or more independent background
    # processes. Maybe a complex message queue.
    app = current_app._get_current_object()
    msg = Message(subject,
                  sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

    return thr


################################################################################
# flask route
@app.before_request
def before_request():
    # for some key access points, check the status of sign in
    if request.path in ('/file_list.html',
                        '/changepassword',
                        '/change_password.html'):
        if 'email' not in session:
            # to the page of 'sign in' if did not sign in
            return redirect('index.html')


@app.route('/')
def index():
    if 'email' in session:
        return redirect('file_list.html')
    else:
        return redirect('index.html')


@app.route('/signin', methods=['POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        rememberme = request.form.get('remember-me')

        # the json data to front-end
        data = {}

        # ! the original password is not in database !
        md5 = hashlib.md5(password.encode(encoding='utf-8')).hexdigest()
        user = User.query.filter_by(email=email,
                                    password=md5,
                                    activity=1).first()
        if user:
            # there is the user
            # save the email in session as the passport
            session['email'] = email

            if 'true' == rememberme:
                # a long time session
                session.permanent = True
                # app.permanent_session_lifetime = timedelta(hours=1)
            else:
                # a temporary session
                session.permanent = False

            data['success'] = True
            data['url'] = 'file_list.html'
        else:
            # cannot find the user
            data['success'] = False
            data['errmsg'] = 'this user does not exist or incorrect password'

        return json.dumps(data, ensure_ascii=False)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('index.html')


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # the json data to front-end
        data = {}

        user = User.query.filter_by(email=email).first()
        if user:
            data['success'] = False
            data['errmsg'] = 'this email has existed'
            return json.dumps(data, ensure_ascii=False)

        # !!! Do NOT save the ORIGINAL password !!!
        # Because lots people have just one password for every situation.
        password_md5 = hashlib.md5(
            password.encode(encoding='utf-8')).hexdigest()

        # the user should use this code to active their accounts
        activecode = str(uuid.uuid1())

        user = User(email=email, password=password_md5,
                    activecode=activecode, activity=0)
        db.session.add(user)
        db.session.commit()

        # send activecode to user's email
        # protocol or domain if there is one
        email_body = app.config['PROTOCOL'] + \
            '://' + \
            app.config['IP'] + \
            ':' + \
            str(app.config['PORT']) + \
            '/active/' + activecode

        send_email(email, 'Active your account from Rosetta Stone', email_body)

        data['success'] = True
        data['url'] = 'index.html'

        return json.dumps(data, ensure_ascii=False)


@app.route('/active/<activecode>')
def active(activecode):
    # there is the activecode and the user is not active
    user = User.query.filter_by(activecode=activecode,
                                activity=0).first()
    if user:
        # the user is active now
        user.activity = 1
        db.session.commit()

    return redirect('index.html')


@app.route('/changepassword', methods=['POST'])
def changepassword():
    if request.method == 'POST':
        password = request.form.get('password')
        new_password = request.form.get('new-password')

        # the json data to the front-end
        data = {}

        md5_password = \
            hashlib.md5(password.encode(encoding='utf-8')).hexdigest()
        user = User.query.filter_by(email=session['email'],
                                    password=md5_password,
                                    activity=1).first()
        if user:
            md5_newpassword = \
                hashlib.md5(new_password.encode(encoding='utf-8')).hexdigest()
            user.password = md5_newpassword
            db.session.commit()

            data['success'] = True
            data['errmsg'] = 'Password has been changed!'
        else:
            data['success'] = False
            data['errmsg'] = 'Change password failed!'

        return json.dumps(data, ensure_ascii=False)


################################################################################
# flask start


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


app.config['PROTOCOL'] = 'http'   # https
app.config['IP'] = get_host_ip()  # or '0.0.0.0'
app.config['PORT'] = 8088         # or https-8443
app.run(host=app.config['IP'], port=app.config['PORT'], debug=False)
# app.run(host=app.config['IP'], port=8443, ssl_context='adhoc', debug=False)
