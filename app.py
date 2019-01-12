from flask import Flask, request, render_template,url_for,redirect,session, jsonify, flash
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from forms import (signIn_form_People, signIn_form_Company,login_form, insert_job, editProfile,
                   location_job, RequestResetForm, ResetPasswordForm)
from datetime import date, datetime, timedelta
from flask_login import login_user, current_user, logout_user, login_required, UserMixin, LoginManager
from dotenv import load_dotenv
import dialogflow
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail, Message

from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER_CONTRACT = 'static/company/contracts'
UPLOAD_FOLDER_SIGN = 'static/user/signs'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
MAX_CONTENT_PATH = '5120'

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['UPLOAD_FOLDER_CONTRACT'] = UPLOAD_FOLDER_CONTRACT
app.config['UPLOAD_FOLDER_SIGN'] = UPLOAD_FOLDER_SIGN
mail = Mail(app)
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    if session['company']:
        return Company.query.get(int(user_id))
    return Person.query.get(int(user_id))


class Job(db.Model):
    __tablename__ = "Job"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)
    description = db.Column(db.Text(100), nullable=True)
    datework = db.Column(db.String(26), nullable=True)
    dayOfWeek = db.Column(db.String(10), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('Company.id'), nullable=True)
    places = db.Column(db.Integer, nullable=True)
    location = db.Column(db.String(20), nullable=True)
    time_slot = db.Column(db.Integer, nullable=True)
    wage = db.Column(db.Float, nullable=True)
    available = db.Column(db.Boolean, nullable=True, default=True)
    contract = db.Column(db.String(30), nullable=True, default='example.jpg')


class JobPerson(db.Model):
    __tablename__ = "JobPerson"
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('Job.id'), nullable=True)
    person_id = db.Column(db.Integer, db.ForeignKey('Person.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=True)


class Person(db.Model, UserMixin):
    __tablename__ = 'Person'
    id=db.Column(db.Integer,primary_key=True)
    person_no=db.Column(db.String(20),unique=True,nullable=True)
    name = db.Column(db.String(10), nullable=True)
    surname = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    email=db.Column(db.String(20),unique=True,nullable=True)
    password=db.Column(db.String(30),nullable=True)
    IBAN=db.Column(db.String(31), nullable=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Person.query.get(user_id)


    def __repr__(self):
        return "<Person %r>" % self.name


class Company(db.Model, UserMixin):
    __tablename__ = 'Company'
    id=db.Column(db.Integer,primary_key=True)
    company_no=db.Column(db.String(20),unique=True,nullable=True)
    name = db.Column(db.String(10), nullable=True)
    telephone = db.Column(db.Integer, nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    email=db.Column(db.String(20),unique=True,nullable=True)
    password=db.Column(db.String(30),nullable=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Company.query.get(user_id)

    def __repr__(self):
        return "<Company %r>" % self.name


@app.before_first_request
def setup_db():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', title='JON')


@app.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editprofile():

    form_edit = editProfile()
    if session['company']:
        st = Company.query.filter_by(email=session['email']).first()
    else:
        st = Person.query.filter_by(email=session['email']).first()

    if request.method == 'POST' and session['company']:
        if session['id']:
            company = Company.query.get(session['id'])
            company.name = request.form['name']
            company.phone = request.form['phone']
            company.email = request.form['email']
            db.session.commit()
            return redirect(url_for('companypage'))
        else:
            return redirect(url_for('index'))
    if request.method == 'POST' and session['company']==False:
        if session['id']:
            person = Person.query.get(session['id'])
            person.name = request.form['name']
            person.phone = request.form['phone']
            person.email = request.form['email']
            person.IBAN = request.form['bankaccount']
            db.session.commit()
            return redirect(url_for('userprofile'))
        else:
            redirect(url_for('index'))

    return render_template('editprofile.html', title='Edit', st=st,company=session['company'], form_edit=form_edit)


@app.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        if session['company']:
            return redirect(url_for('companypage'))
        else:
            return redirect(url_for('userpage'))

    form_login=login_form()
    if form_login.validate_on_submit():
        st = Person.query.filter_by(email=form_login.email.data).first()
        company = False
        if st is None:
            st = Company.query.filter_by(email=form_login.email.data).first()
            company = True
        if st and bcrypt.check_password_hash(st.password, form_login.password.data):
            session['email'] = form_login.email.data
            session['id'] = st.id
            session['company'] = company
            login_user(st)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            elif session['company']:
                return redirect(url_for('companypage'))
            else:
                return redirect(url_for('userpage'))
        else:
            flash('Login Error')
    return render_template('login.html',formpage = form_login, title='SignIn')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/newjob',methods=['POST','GET'])
@login_required
def newjob():
    if not session['company']:
        return redirect(url_for('index'))
    form_newjob = insert_job()

    new_job = insert_job()
    # if new_job.validate_on_submit():
    if request.method == 'POST':
        day = get_day(new_job.datework.data.weekday())
        print(get_day(new_job.datework.data.weekday()))
        job = Job(
            name=new_job.name.data,
            description=new_job.description.data,
            location=new_job.location.data.upper(),
            datework=new_job.datework.data,
            places=new_job.places.data,
            time_slot=new_job.time.data,
            wage=new_job.salary.data,
            dayOfWeek=day,
            company_id=session['id']

        )
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('companypage'))

    return render_template('newjob.html', formpage=form_newjob, title='NewJob')


@app.route('/editjob/<job_id>', methods=['GET', 'POST'])
@login_required
def editjob(job_id):
    if not session['company']:
        pass
    job = Job.query.get(job_id)
    form = insert_job()
    
    if request.method=='POST':
        job.name=form.name.data
        job.description=form.description.data
        job.location=form.location.data.upper()
        job.datework=form.datework.data
        job.places=form.places.data
        job.time_slot=form.time.data
        job.wage=form.salary.data
        job.company_id=session['id']
        db.session.commit()
        return redirect((url_for('job', job_id=str(job.id))))
    return render_template('editjob.html', title="Edit Job", formpage=form, job=job)
    

@app.route('/signup')
def signup():
    return render_template('signuptype.html', title='SignIn')

@app.route('/signuptype')
def signuptype():
    return render_template('signuptype.html', title='SignIn')


@app.route('/signupCompany',methods=['POST', 'GET', 'PUT'])
def signupCompany():
    form_company=signIn_form_Company()
    if form_company.validate_on_submit():
        password=bcrypt.generate_password_hash(form_company.password.data).decode('utf-8')
        # noinspection PyArgumentList
        register=Company(
                        name=form_company.name.data,
                        phone=form_company.phone.data,
                        email=form_company.email.data,
                        password=password
        )
        db.session.add(register)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signupCompany.html',formpage = form_company, title='SignIn')


@app.route('/signupPerson',methods=['POST','GET', 'PUT'])
def signupPerson():
    form_person=signIn_form_People()
    if form_person.validate_on_submit():
        password=bcrypt.generate_password_hash(form_person.password.data).decode('utf-8')
        # noinspection PyArgumentList
        register=Person(
                        name=form_person.name.data,
                        surname=form_person.surname.data,
                        phone=form_person.phone.data,
                        email=form_person.email.data,
                        password=password,
                        IBAN=form_person.bankaccount.data
        )
        db.session.add(register)
        db.session.commit()
        return redirect(url_for('login'))


    return render_template('signupPerson.html',formpage = form_person, title='SignIn')


@app.route('/userpage', methods=['GET', 'POST'])
def userpage():
    # if a company is logged in, it can't open this page
    if session['company']:
        return redirect(url_for('companypage'))
    loc= ''
    search_form = location_job()
    if request.method=='POST' and search_form.validate_on_submit():
        loc = search_form.location.data.upper()

    startDate = date.today()
    offset = timedelta(days=6)
    mon = timedelta(days=startDate.isoweekday() - 1)
    startDate = startDate-mon
    endDate = startDate + offset

    print('Start date: ' + str(startDate))
    print('End date: ' + str(endDate))
    # Get all jobs from db
    if loc == '':
        jobs = Job.query.filter_by(available=True).all()
    else:
        jobs = Job.query.filter_by(location=loc).filter_by(available=True).all()
    # Get jobs already booked by logged account
    jobs_booked = Job.query.join(JobPerson).filter_by(person_id=session['id']).all()
    # Remove booked jobs from job list
    jobs = [item for item in jobs if item not in jobs_booked]
    # Check start and end date
    tmp = []
    for job in jobs:
        if parse_date(job.datework).date() < startDate or parse_date(job.datework).date() > endDate:
            tmp.append(job)
    # Remove jobs not in current week
    jobs = [x for x in jobs if x not in tmp]

    joblist = []
    for i in range(0, 24):
        tmp = []
        for job in jobs:
            if job.time_slot == i:
                tmp.append(job)
        joblist.append(tmp)

    return render_template('userpage.html',  email=session.get('email',False) , title='userPage', jobs=joblist, form=search_form)


@app.route('/userprofile')
@login_required
def userprofile():
    if session['company']:
        return redirect(url_for('companypage'))
    # Get current day
    startDate = date.today()
    offset = timedelta(days=6)
    # Get day Monday of current week
    mon = timedelta(days=startDate.isoweekday() - 1)
    startDate = startDate - mon
    endDate = startDate+offset

    # person = Person.query.filter_by(email=session['email']).first()
    jobs = Job.query.join(JobPerson).filter(JobPerson.person_id==session['id']).all()
    tmp = []
    for job in jobs:
        if parse_date(job.datework).date() < startDate or parse_date(job.datework).date() > endDate:
            tmp.append(job)
    jobs = [x for x in jobs if x not in tmp]

    joblist = []
    for i in range(0, 24):
        tmp = []
        for job in jobs:
            if job.time_slot == i:
                tmp.append(job)
        joblist.append(tmp)

    return render_template('userprofile.html', email=session.get('email',False) , title='userProfile', jobs=joblist)


@app.route('/companypage')
def companypage():
    if not session['company']:
        return redirect(url_for('userpage'))
    # company = Company.query.filter_by(email=session['email']).first()
    jobs = Job.query.join(Company).filter(Company.id == session['id']).all()
    joblist = []
    for i in range(0, 24):
        tmp = []
        for job in jobs:
            if job.time_slot == i:
                tmp.append(job)
        joblist.append(tmp)

    return render_template('companyPage.html', title='companyPage', jobs=joblist)


@app.route('/job', defaults={'job_id': 0}, methods=['GET','POST'])
@app.route('/job/<job_id>', methods=['GET','POST','PUT','DELETE'])
@login_required
def job(job_id):

    if request.method=='GET':
        if job_id == 0:
            return jsonify(isError=True,
                           message="Missing job id",
                           statusCode=400), 400
        selected_job = Job.query.filter_by(id=job_id).first()
        company_name = Company.query.get(selected_job.company_id)
        rating = False
        bookable = True
        if session['company']:
            if parse_date(selected_job.datework).date() < date.today():
                rating = True
        else:
            if JobPerson.query.filter_by(job_id=job_id, person_id=session['id']).first():
                bookable=False

        return render_template('jobDescription.html', job=selected_job, title='Description', bookable=bookable, company=session['company'], rating=rating, companyname=company_name)

        new_job = insert_job()
        # if new_job.validate_on_submit():
        if request.method == 'POST':
            if not session['company']:
                return redirect(url_for('userpage'))
            day = get_day(new_job.datework.data.weekday())
            print(get_day(new_job.datework.data.weekday()))
            job = Job(
                name=new_job.name.data,
                description=new_job.description.data,
                datework=new_job.datework.data,
                dayOfWeek=day,
                places=new_job.places.data,
                company_id=session['id'],
                location=new_job.location.data.upper()
            )
            db.session.add(job)
            db.session.commit()
            return jsonify(isError=False,
                           message="Success",
                           statusCode=201), 201

    if request.method=='PUT':
        if job_id == 0:
            return jsonify(isError=True,
                           message="Missing job id",
                           statusCode=400), 400
        return True
        # TODO insert the modify job here

    if request.method=='DELETE':
        if job_id == 0:
            return jsonify(isError=True,
                           message="Missing job id",
                           statusCode=400), 400
        selected_job = JobPerson.query.filter_by(job_id=job_id).first()
        if selected_job:
            return jsonify(isError=True,
                           message="This job is already booked, you can not delete this",
                           statusCode=304), 304
        selected_job = Job.query.filter_by(id=job_id).first()
        if selected_job:
            db.session.delete(selected_job)
            db.session.commit()
            return jsonify(isError=False,
                           message="Job deleted",
                           statusCode=204), 204
        return jsonify(isError=True,
                       message="No job to delete founded",
                       statusCode=404), 404


@app.route('/bookjob/<job_id>', methods=['GET','POST','DELETE'])
@login_required
def bookjob(job_id):
    if request.method=='POST':
        if session['company']:
            return jsonify(isError=True,
                           message="Company can not book a job",
                           statusCode=401), 401
        print(job_id)
        places_booked = JobPerson.query.filter_by(job_id=job_id).count()
        job = Job.query.filter_by(id=job_id).first()
        print('person in this job: '+str(places_booked))
        if places_booked != job.places:
            book = JobPerson(
                person_id = session['id'],
                job_id = job_id
            )
            if (places_booked+1) == job.places:
                job.available = False
            db.session.add(book)
            db.session.commit()
            print('Job booked successfully!')
            return jsonify(isError=False,
                           message="Job booked",
                           statusCode=200), 200
        else:
            return jsonify(isError=True,
                           message="Job full booked",
                           statusCode=200), 200
    if request.method == 'DELETE':
        selected_job = JobPerson.query.filter_by(job_id=job_id, person_id=session['id']).first()
        job = Job.query.get(job_id)
        job.available = True
        db.session.delete(selected_job)
        db.session.commit()
        return jsonify(isError=False,
                       message="Job unbooked",
                       statusCode=204), 204
    return jsonify(isError=True,
                   message="No action",
                   statusCode=404), 404


# TODO interface for bot assistance (dedicated page or chat facebook-like)
@app.route('/help')
def help():
    return render_template('help.html')


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)

        return response.query_result.fulfillment_text


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }

    return jsonify(response_text)


@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        message = request.form['message']
        print(message)
        msg = Message('CONTACT US',
                      sender='jonpolito2018@gmail.com',
                      recipients=['jonpolito2018@gmail.com'])
        msg.body = message
        mail.send(msg)
        return redirect(url_for('contact'))


def send_reset_email(user):
    token = user.get_reset_token()

    msg = Message('Password Reset Request',
                  sender='jonpolito2018@gmail.com',
                  recipients=[user.email])
    msg.body = "To reset your password, visit the following link:\n" \
               "{url}\n\n" \
               "If you did not make this request simply ignore this email and no change will be made.".format(
                url={url_for('reset_token', token= token, _external=True)})
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        if session['company']:
            return redirect(url_for('companypage'))
        else:
            return redirect(url_for('userpage'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Person.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Company.query.filter_by(email=form.email.data).first()
            if user is None:
                return redirect(url_for('signuptype'))

        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title="Reset Password", formpage=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        if session['company']:
            return redirect(url_for('companypage'))
        else:
            return redirect(url_for('userpage'))

    user = Person.verify_reset_token(token)
    if user is None:
        user = Company.verify_reset_token(token)
        if user is None:
            flash('That is an invalid or expired token', 'warning')
            return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = password
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title="Reset Password", formpage=form)


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('uploadContract.html', title='Contract Upload')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'contract' in request.files:
            file = request.files['contract']
            contract = True

        if 'sign' in request.files:
            file = request.files['sign']
            contract = False
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return jsonify(isError=True,
                           message="Not Uploaded",
                           statusCode=500), 500
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            name = str(session['id']) + '.'+ext
            filename = secure_filename(name)
            if contract:
                jobid = request.form['job']
                job = Job.query.get(jobid)
                job.contract = filename
                db.session.commit()
                file.save(os.path.join(app.config['UPLOAD_FOLDER_CONTRACT'], filename))
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER_SIGN'], filename))
            return jsonify(isError=False,
                       message="Uploaded",
                       statusCode=204), 204

@app.errorhandler(404)#Error pages
def page_not_found(e):
    return render_template('404.html', title='404'),404


# function to parse String like '2018-12-25' in Date type
def parse_date(dateToConvert):
    return datetime.strptime(dateToConvert, '%Y-%m-%d')

def get_day(isoday):
    if isoday==0:
        return 'Monday'
    if isoday==1:
        return 'Tuesday'
    if isoday==2:
        return 'Wednesday'
    if isoday==3:
        return 'Thursday'
    if isoday==4:
        return 'Friday'
    if isoday==5:
        return 'Saturday'
    if isoday==6:
        return 'Sunday'


if __name__ == '__main__':
    app.run(debug=True)
