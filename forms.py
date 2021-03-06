from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, DateField, TextAreaField, IntegerField
from wtforms.validators import Email,DataRequired,Length,EqualTo, ValidationError, NumberRange

class signIn_form_People(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=20)])
    phone= StringField('Phone', validators=[DataRequired(), Length(min=2, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bankaccount = StringField('Bank Account Number', validators=[Length(min=15, max=31)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])
    password_con = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign In')

class signIn_form_Company(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=2, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])
    password_con = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign In')


class editProfile(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=2, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bankaccount = StringField('Bank Account Number', validators=[Length(min=15, max=31)])
    submit = SubmitField('Edit')


class login_form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('LogIn')


class insert_job(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description',validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    datework = DateField('Date', validators=[DataRequired()])
    places = IntegerField('Places available', validators=[DataRequired()])
    time = StringField('Time', validators=[DataRequired])
    salary = StringField('Salary', validators=[DataRequired])
    submit = SubmitField('Add')

class location_job(FlaskForm):
    location = StringField('Location')
    submit = SubmitField('Search')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password_con = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class RateWorkers(FlaskForm):
    rate = IntegerField('Rate', validators=[DataRequired(), NumberRange(min=0, max=9)])
    person_id = IntegerField()
    submit = SubmitField('Rate')
