from flask import Flask, request, render_template,url_for

app = Flask(__name__)


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
    return render_template('userpage.html', title='userPage')

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
