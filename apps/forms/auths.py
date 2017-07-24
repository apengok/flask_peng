from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField,TextAreaField,SelectField
from wtforms.validators import Regexp,Required, Email,Length,DataRequired,EqualTo
from wtforms import ValidationError

from apps.models import Users,Role

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

class PasswordResetRequestForm(FlaskForm):

    email = StringField('Email', validators=[Required(), Length(1, 64),

                                             Email()])

    submit = SubmitField('Reset Password')
    
class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),

                                             Email()])
    password = PasswordField('New Password', validators=[
        Required(),
        EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Repeat Password',validators=[Required()])
    submit = SubmitField('Confirm Change')
    
    def validate_email(self,field):
        if Users.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')
    
class ChangeEmailForm(FlaskForm):
    email = StringField('New Email Address', validators=[Required(),Length(1,64),Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Confirm Change')
    
    def validate_email(self,field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registed.')
            
            
class EditProfileForm(FlaskForm):
    username = StringField('Real name',validators=[Length(0,64)])
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
    
    
class EditProfileAdminForm(FlaskForm):
    username = StringField('Real name',validators=[Required(),Length(0,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                'Usernames must have only letters, '
                                                'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role',coerce=int)
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
    
    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices = [(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
        
    def validate_username(self,field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')