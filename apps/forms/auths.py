from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators,SubmitField
from wtforms.validators import Required, Email,Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
        Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])