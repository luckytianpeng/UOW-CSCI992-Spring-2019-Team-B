"""
CSCI991 Project Spring 2019, UOW
Team B
pt882@uowmail.edu.au
"""

import os
import sys
import json
import socket
import hashlib
import uuid
from threading import Thread
import datetime
import pickle

from flask import Flask
from flask import redirect, request, session, make_response, url_for, send_from_directory
from flask import current_app, render_template
from flask_sqlalchemy import SQLAlchemy
# from werkzeug import secure_filename
from werkzeug.utils import secure_filename
from flask_mail import Mail,Message

import matplotlib
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.contrib import predictor

sys.path.append('../')
import rxrx.io as rio


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
app.config['MAIL_SERVER'] = 'smtp.live.com'  # 'smtp.gmail.com'  #
app.config['MAIL_PORT'] = 25  # 465  #
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# !!! Do NOT put account and password in source !!!
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or ''
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or ''

# uploading files
app.config['ALLOW_EXTENSIONS'] = set(['png'])
app.config['UPLOAD_FOLDER'] = 'uploads'

# model
app.config['MODEL'] = r'D:\_20200313_\_peng\PycharmProjects\csci992\bucket\saved_model\1584067643'

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


class File(db.Model):
    # table : File
    id = db.Column(db.Text, primary_key=True)
    email = db.Column(db.Text, db.ForeignKey('user.email'))
    cell_type = db.Column(db.Text, nullable=False)
    experiment_on = db.Column(db.Text, nullable=False)
    plate_no = db.Column(db.Text, nullable=False)
    well_type = db.Column(db.Text, nullable=False)
    files = db.Column(db.Text, nullable=False)
    rgb_file = db.Column(db.Text, nullable=False)
    submit_time = db.Column(db.Text, nullable=False)
    sirna = db.Column(db.Text, nullable=False)

    def __init__(self, id, email, cell_type, experiment_on, plate_no, well_type, files, rgb_file, submit_time, sirna):
        self.id = id
        self.email = email
        self.cell_type = cell_type
        self.experiment_on = experiment_on
        self.plate_no = plate_no
        self.well_type = well_type
        self.files = files
        self.rgb_file = rgb_file
        self.submit_time = submit_time
        self.sirna = sirna

    def __repr__(self):
        return '<File %>' % self.id

# ##################################################################### database

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

# upload files #################################################################
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOW_EXTENSIONS']
# ################################################################# upload files

# neural network model:
pred = predictor.from_saved_model(app.config['MODEL'])


# utilities ####################################################################

# e.g. 2018-10-06T18:35:57.300245
def isoformat(time):
    if isinstance(time, datetime.datetime):
        return time.isoformat()
    elif isinstance(time, datetime.timedelta):
        hours = time.seconds // 3600
        minutes = time.seconds % 3600 // 60
        seconds = time.seconds % 3600 % 60
        return 'P%sDT%sH%sM%sS' % (time.days, hours, minutes, seconds)

# #################################################################### utilities

################################################################################
# flask route
@app.before_request
def before_request():
    # for some key access points, check the status of sign in
    if request.path in ('/file_list.html',
                        'submit_file.html',
                        '/changepassword',
                        '/change_password.html',
                        '/upload'):
        if 'email' not in session:
            # to the page of 'sign in' if did not sign in
            return redirect('index.html')
    else:
        head_tail = os.path.split(request.path)
        if head_tail[0][1:] == app.config['UPLOAD_FOLDER']:
            if 'email' in session:
                return make_response(send_from_directory(head_tail[0][1:], head_tail[1]))


TR_FORMAT = \
    '''<tr>
        <td class="info">
            <p class="cell_type">Cell: %s</p>
            <p class="experiment_on">Exp: %s</p>
            <p class="plate_no">Plate: %s</p>
            <p class="well_type">Well Type: %s</p>
            <p class="submit_time">Submit: %s</p>
            <p class="sirna">Sirna: %s</p>
        </td>
        <td class="channels">%s</td>
    </tr>'''


@app.route('/filelist', methods=['POST'])
def filelist():
    # file list info to the front-end
    file_list = ''

    # all the file which belong to the user
    record = File.query.filter_by(email=session['email'])
    for r in record:
        images = ('<img alt="imgs" src="%s/%s" class="rgb" />'
                   % (app.config['UPLOAD_FOLDER'], r.rgb_file))

        images = ('<img class="rgb" src="%s/%s" alt="Photo landscape">' % (app.config['UPLOAD_FOLDER'], r.rgb_file) )

        for f in r.files.split(','):
            images += ('<img alt="imgs" src="%s/%s" class="channel" />'
                       % (app.config['UPLOAD_FOLDER'], f))

        file_list += (
                TR_FORMAT % (r.cell_type,
                             r.experiment_on,
                             r.plate_no,
                             r.well_type,
                             r.submit_time,
                             r.sirna,
                             images
                             ))
        file_list += '\n'

    data = {}
    data['success'] = True
    data['file_list'] = file_list

    return json.dumps(data, ensure_ascii=False)


@app.route('/upload', methods=['POST'])
def upload():
    print('--> /upload')
    if 'POST' == request.method:
        HEPG2 = request.form.get('radio-choice-h-2a')
        HVUEC = request.form.get('radio-choice-h-2b')
        RPE = request.form.get('radio-choice-h-2c')
        U2OS = request.form.get('radio-choice-h-2d')

        cell_type = ''
        if HEPG2:
            cell_type = 'HEPG2'
        elif HVUEC:
            cell_type = 'HVUEC'
        elif RPE:
            cell_type = 'RPE'
        else:
            cell_type = 'U2OS'

        experiment_on = request.form.get('experiment-no')
        plate_no = request.form.get('plate-no')

        positive_control = request.form.get('well-radio-choice-h-2')
        negative_control = request.form.get('well-radio-choice-h-2b')
        treatment = request.form.get('well-radio-choice-h-2c')
        well_type = ''
        if positive_control:
            well_type  = 'positive_control'
        elif negative_control:
            well_type = 'negative_control'
        else:
            well_type = 'treatment'

        print(HEPG2, HVUEC, RPE, U2OS)
        print(experiment_on)

        files = []
        rgb_file_name = ''
        for file in request.files.getlist('files'):
            if file and allowed_file(file.filename):
                filename = cell_type + '-' + experiment_on \
                           + '-Plate' + plate_no \
                           + '-' + secure_filename(file.filename)
                print('-->', file.filename, '==>', filename)

                t = filename.split('_')
                rgb_file_name = t[0] + '_rgb.png'

                files.append(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # load
        channel_paths = [os.path.join(app.config['UPLOAD_FOLDER'], f) for f in files]
        tensor = rio.load_images_as_tensor(channel_paths)
        #
        rgb = rio.convert_tensor_to_rgb(tensor)
        rgb = np.array(rgb, dtype=np.uint8)
        matplotlib.image.imsave(os.path.join(app.config['UPLOAD_FOLDER'], rgb_file_name), rgb)
        # predict:
        tensor = np.expand_dims(tensor, axis=0)
        predictions = pred({'feature': tensor})

        print(predictions)

        id = str(uuid.uuid1())
        submit_time = isoformat(datetime.datetime.now())

        # save file to database
        record_file = File(id,
                           session['email'],
                           cell_type,
                           experiment_on,
                           plate_no,
                           well_type,
                           ','.join(files),
                           rgb_file_name,
                           submit_time,
                           '%d' % predictions['classes'][0])
        db.session.add(record_file)
        db.session.commit()

    return redirect('file_list.html')


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

        send_email(email, 'Active your PI account ', email_body)

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

    return redirect('/index.html')


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
