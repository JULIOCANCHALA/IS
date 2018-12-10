from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField
from wtforms.validators import Email,DataRequired,Length,EqualTo

class signIn_form_People(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=20)])
    phone= StringField('Phone', validators=[DataRequired(), Length(min=2, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])
    password_con = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('SigIn')

class signIn_form_Company(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    telephone= StringField('Telephone', validators=[DataRequired(), Length(min=2, max=10)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=2, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])
    password_con = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('SigIn')


class login_form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('LogIn')