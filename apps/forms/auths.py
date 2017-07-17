from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import Regexp,Required, Email,Length,DataRequired,EqualTo
from wtforms import ValidationError

from apps.models import Users

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
        Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Required(),Length(min=4, max=25),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
            'Usernames must have only letters, '
            'numbers, dots or underscores')])
    email = StringField('Email Address', validators=[Required(),Length(1,64),Email()])
    password = PasswordField('Password', validators=[
        Required(),
        EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Repeat Password',validators=[Required()])
    accept_tos = BooleanField('I accept the TOS', [DataRequired()])
    submit = SubmitField('Register')
    
    #When a form defines a method with the prefix validate_ followed by the name of a field, the method is invoked in addition to any regularly defined validators.

    def validate_email(self,field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
            
    def validate_username(self,field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
    
    
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password',validators=[Required()])
    password = PasswordField('New Password', validators=[
        Required(),
        EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Repeat Password',validators=[Required()])
    submit = SubmitField('Confirm Change')
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        Required(),
        EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Repeat Password',validators=[Required()])
    submit = SubmitField('Confirm Change')
    
class ChangeEmailForm(FlaskForm):
    old_password = PasswordField('Old Password',validators=[Required()])
    password = PasswordField('New Password', validators=[
        Required(),
        EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Repeat Password',validators=[Required()])
    submit = SubmitField('Confirm Change')