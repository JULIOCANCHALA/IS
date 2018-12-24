from flask import Flask, request, render_template,url_for,redirect,session, jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from forms import signIn_form_People, signIn_form_Company,login_form, insert_job
from datetime import date, datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'cvbnmjhgfdcvbnmnbv'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlweb.db'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)

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


class Person(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    person_no=db.Column(db.String(20),unique=True,nullable=True)
    name = db.Column(db.String(10), nullable=True)
    surname = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    email=db.Column(db.String(20),unique=True,nullable=True)
    password=db.Column(db.String(30),nullable=True)

    def __repr__(self):
        return "<Person %r>" % self.name

class Company(db.Model):
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
def loginpage():
    form_login=login_form()
    if form_login.validate_on_submit():
        st = Person.query.filter_by(email=form_login.email.data).first()
        if not st:
            st = Company.query.filter_by(email=form_login.email.data).first()
        if st and bcrypt.check_password_hash(st.password, form_login.password.data):
            session['email'] = form_login.email.data
            return redirect(url_for('userpage'))
    return render_template('login.html',formpage = form_login, title='SignIn')

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
def userpage():

    startDate = date.today()
    startDate = startDate.replace(day=startDate.day - startDate.weekday())
    endDate = startDate.replace(day=startDate.day + 6)
    print('Start date: ' + str(startDate))
    print('End date: ' + str(endDate))
    # jobs = Job.query.filter(parse_date(Job.datework) > startDate).all()
    jobs = Job.query.all()

    tmp = []
    for job in jobs:
        if parse_date(job.datework).date() < startDate or parse_date(job.datework).date() > endDate:
            tmp.append(job)
    jobs = [x for x in jobs if x not in tmp]

    return render_template('userpage.html',  email=session.get('email',False) , title='userPage', jobs=jobs)

@app.route('/userprofile')
def userprofile():
    person = Person.query.filter_by(email=session['email']).first()
    jobs = Job.query.join(JobPerson).filter(JobPerson.person_id==person.id).all()

    return render_template('userprofile.html', email=session.get('email',False) , title='userProfile', jobs=jobs)

@app.route('/companypage')
def companypage():
    company = Company.query.filter_by(email=session['email']).first()
    jobs = Job.query.join(Company).filter(Company.id == company.id).all()

    return render_template('companyPage.html', title='companyPage', jobs=jobs)


@app.route('/newjob', methods=['GET', 'POST'])
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
    if request.method=='POST':
        print(job_id)
        # person = Person.query.filter_by(email=session['email']).first()
        person = Person(
            id = 1
        )

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

    return render_template('index.html', title='JON')

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
