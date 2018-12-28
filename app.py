from flask import Flask, request, render_template,url_for,redirect,session, jsonify, flash
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from forms import signIn_form_People, signIn_form_Company,login_form, insert_job
from datetime import date, datetime
from flask_login import login_user, current_user, logout_user, login_required, UserMixin, LoginManager
import os
from dotenv import load_dotenv
import dialogflow

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return Person.query.get(int(user_id))

class Job(db.Model):
    table = "Job"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)
    description = db.Column(db.Text(100), nullable=True)
    datework = db.Column(db.String(26), nullable=True)
    dayOfWeek = db.Column(db.String(10), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    places = db.Column(db.Integer, nullable=True)


class JobPerson(db.Model):
    table = "JobPerson"
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=True)


class Person(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    person_no=db.Column(db.String(20),unique=True,nullable=True)
    name = db.Column(db.String(10), nullable=True)
    surname = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    email=db.Column(db.String(20),unique=True,nullable=True)
    password=db.Column(db.String(30),nullable=True)

    def __repr__(self):
        return "<Person %r>" % self.name

class Company(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    company_no=db.Column(db.String(20),unique=True,nullable=True)
    name = db.Column(db.String(10), nullable=True)
    telephone = db.Column(db.Integer, nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    email=db.Column(db.String(20),unique=True,nullable=True)
    password=db.Column(db.String(30),nullable=True)

    def __repr__(self):
        return "<Company %r>" % self.name



@app.before_first_request
def setup_db():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', title='JON')

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
        session['company'] = False
        if not st:
            st = Company.query.filter_by(email=form_login.email.data).first()
            session['company'] = True
        if st and bcrypt.check_password_hash(st.password, form_login.password.data):
            session['email'] = form_login.email.data
            login_user(st,False)
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
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup')
def signup():
    return render_template('signuptype.html', title='SignIn')

@app.route('/signuptype')
def signuptype():
    return render_template('signuptype.html', title='SignIn')


@app.route('/signupCompany',methods=['POST','GET'])
def signupCompany():
    form_company=signIn_form_Company()
    if form_company.validate_on_submit():
        password=bcrypt.generate_password_hash(form_company.password.data)
        register=Company(
                        name=form_company.name.data,
                        telephone=form_company.telephone.data,
                        phone=form_company.phone.data,
                        email=form_company.email.data,
                        password=password
        )
        session['email'] = register.email
        db.session.add(register)
        db.session.commit()
        return redirect(url_for('companypage'))
    return render_template('signupCompany.html',formpage = form_company, title='SignIn')


@app.route('/signupPerson',methods=['POST','GET'])
def signupPerson():
    form_person=signIn_form_People()
    if form_person.validate_on_submit():
        password=bcrypt.generate_password_hash(form_person.password.data)
        register=Person(
                        name=form_person.name.data,
                        surname=form_person.surname.data,
                        phone=form_person.phone.data,
                        email=form_person.email.data,
                        password=password
        )
        session['email'] = register.email
        db.session.add(register)
        db.session.commit()
        return redirect(url_for('userpage'))
    return render_template('signupPerson.html',formpage = form_person, title='SignIn')

@app.route('/userpage')
@login_required
def userpage():
    person = Person.query.filter_by(email=session['email']).first()
    # Get current week
    startDate = date.today()
    startDate = startDate.replace(day=startDate.day - startDate.weekday())
    endDate = startDate.replace(day=startDate.day + 6)
    print('Start date: ' + str(startDate))
    print('End date: ' + str(endDate))
    # Get all jobs from db
    jobs = Job.query.all()
    # Get jobs already booked by logged account
    jobs_booked = Job.query.join(JobPerson).filter_by(person_id=person.id).all()
    # Remove booked jobs from job list
    jobs = [item for item in jobs if item not in jobs_booked]
    # Check start and end date
    tmp = []
    for job in jobs:
        if parse_date(job.datework).date() < startDate or parse_date(job.datework).date() > endDate:
            tmp.append(job)
    # Remove jobs not in current week
    jobs = [x for x in jobs if x not in tmp]

    return render_template('userpage.html',  email=session.get('email',False) , title='userPage', jobs=jobs)

@app.route('/userprofile')
@login_required
def userprofile():
    startDate = date.today()
    startDate = startDate.replace(day=startDate.day - startDate.weekday())
    endDate = startDate.replace(day=startDate.day + 6)
    person = Person.query.filter_by(email=session['email']).first()
    jobs = Job.query.join(JobPerson).filter(JobPerson.person_id==person.id).all()
    tmp = []
    for job in jobs:
        if parse_date(job.datework).date() < startDate or parse_date(job.datework).date() > endDate:
            tmp.append(job)
    jobs = [x for x in jobs if x not in tmp]

    return render_template('userprofile.html', email=session.get('email',False) , title='userProfile', jobs=jobs)

@app.route('/companypage')
@login_required
def companypage():
    company = Company.query.filter_by(email=session['email']).first()
    jobs = Job.query.join(Company).filter(Company.id == company.id).all()

    return render_template('companyPage.html', title='companyPage', jobs=jobs)


@app.route('/newjob', methods=['GET', 'POST'])
@login_required
def newjob():
    new_job = insert_job()
    #if new_job.validate_on_submit():
    if request.method == 'POST':
        day = get_day(new_job.datework.data.weekday())
        print(get_day(new_job.datework.data.weekday()))
        # TODO get company ID by session
        job=Job(
            name=new_job.name.data,
            description=new_job.description.data,
            datework=new_job.datework.data,
            dayOfWeek= day,
            places=new_job.places.data,
            company_id=1
        )
        db.session.add(job)
        db.session.commit()
        return jsonify(isError= False,
                    message= "Success",
                    statusCode= 201), 201
    else:
        return redirect(url_for('userpage'))


@app.route('/bookjob/<job_id>', methods=['GET','POST','DELETE'])
def bookjob(job_id):
    person = Person.query.filter_by(email=session['email']).first()
    if request.method=='POST':
        print(job_id)
        places_booked = JobPerson.query.filter_by(job_id=job_id).count()
        job = Job.query.filter_by(id=job_id).first()
        print('person in this job: '+str(places_booked))
        if places_booked != job.places:
            book = JobPerson(
                person_id = person.id,
                job_id = job_id
            )
            db.session.add(book)
            db.session.commit()
            print('Job booked successfully!')
            return redirect(url_for('userpage'))
        else:
            return jsonify(isError=True,
                           message="Job full booked",
                           statusCode=200), 200
    if request.method=='GET':
        selected_job = Job.query.filter_by(id=job_id).first()
        return jsonify(isError=False,
                       message="Success",
                       statusCode=200,
                       data=str(selected_job)), 200

    if request.method=='DELETE':
        selected_job = JobPerson.query.filter_by(job_id=job_id, person_id=person.id).first()
        db.session.delete(selected_job)
        db.session.commit()
        return jsonify(isError=False,
                       message="Job unbooked",
                       statusCode=201), 201

    return render_template('index.html', title='JON')

# TODO interface for bot assistance (dedicated page or chat facebook-like)
@app.route('/chat')
def chat():
    return render_template('chat.html')


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
