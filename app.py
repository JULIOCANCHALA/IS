from flask import Flask, request, render_template,url_for,redirect,session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hakunamatata123456789'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sqlweb.db'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)


class Person(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    person_no=db.Column(db.String(20),unique=True,nullable=True)
    name = db.Column(db.String(10), nullable=True)
    surname = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    email=db.Column(db.String(20),unique=True,nullable=True)
    password=db.Column(db.String(30),nullable=True)
    role_id=db.Column(db.Integer,db.ForeignKey('role.id'),nullable=True)


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
    role_id=db.Column(db.Integer,db.ForeignKey('role.id'),nullable=True)

    def __repr__(self):
        return "<Company %r>" % self.name

class Role(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(10),nullable=True)
    persons=db.relationship('Person',backref='role',lazy=True)
    companies = db.relationship('Company', backref='role', lazy=True)

    def __repr__(self):
        return "<Role %r>" % self.name

from forms import signIn_form_People, signIn_form_Company,login_form

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
        pass_check = bcrypt.generate_password_hash(form_login.password.data).decode('utf-8')
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
                        password=password,
                        role_id=2
        )
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
                        password=password,
                        role_id=1
        )
        db.session.add(register)
        db.session.commit()
        return redirect(url_for('userpage'))
    return render_template('signupPerson.html',formpage = form_person, title='SignIn')

@app.route('/userpage')
def userpage():
    return render_template('personPage.html', email=session.get('email', False), title='Userpage')

@app.route('/userprofile')
def userprofile():
    return render_template('personProfile.html', title='userProfile')

@app.route('/companypage')
def companypage():
    return render_template('companyPage.html', title='companyPage')

@app.errorhandler(404)#Error pages
def page_not_found(e):
    return render_template('404.html', title='404'),404


if __name__ == '__main__':
    app.run(debug=True)
