from flask import Flask, request, render_template,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jondatabase.db'
db = SQLAlchemy(app)


class Worker(db.Model):
    table = "Worker"
    id = db.Column(db.Integer, primary_key=True)


class Company(db.Model):
    table = "Company"
    id = db.Column(db.Integer, primary_key=True)


class Job(db.Model):
    table = "Job"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)
    description = db.Column(db.Text(100), nullable=True)
    date = db.Column(db.String(26), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)


class JobWorker(db.Model):
    table = "JobWorker"
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=True)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable=True)


@app.before_first_request
def setup():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html', title='JON')


@app.route('/login')
def login():
    return render_template('login.html', title='LogIn')


@app.route('/signup')
def signup():
    return render_template('signuptype.html', title='SignIn')


@app.route('/signuptype')
def signuptype():
    return render_template('signuptype.html', title='SignIn')


@app.route('/signupCompany')
def signupperson():
    return render_template('signupCompany.html', title='SignIn')


@app.route('/signupPerson')
def signupcompany():
    return render_template('signupPerson.html', title='SignIn')


@app.route('/userpage')
def userpage():
    
    jobs = Job.query.all()

    return render_template('userpage.html', title='userPage', jobs=jobs)


@app.route('/userprofile')
def userprofile():
    return render_template('userprofile.html', title='userProfile')


@app.route('/companypage')
def companypage():
    return render_template('companyPage.html', title='companyPage')


@app.errorhandler(404)#Error pages
def page_not_found(e):
    return render_template('404.html', title='404'),404


if __name__ == '__main__':
    app.run()
