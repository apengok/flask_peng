from datetime import datetime
from flask import Blueprint,render_template,url_for,redirect,session,request,flash
from flask_login import login_user,logout_user,login_required

from apps.forms.auths import RegistrationForm,LoginForm
#from .. import db
from apps import db
from apps.models import Users

from apps.email import send_email


mod = Blueprint('auth',__name__)

@mod.route('/auth/')
def index():
    return render_template('index.html')

@mod.route('/auth/login/',methods=['GET','POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('blog.index'))
        flash('Invalid username or password.')
        
    return render_template('auth/login.html',form=form)

    
@mod.route('/auth/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('cms.index'))

@mod.route('/auth/register/',methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    
    if request.method == 'POST' and form.validate():
        user = Users(username=form.username.data, password=form.password.data,email=form.email.data,
        )
        
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email,'Confirm Your Account',
                'auth/email/confirm',user=user,token=token)
                
        flash('A confirmation email has been sent to you by email')
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)
    
@mod.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account.Thanks!')
    else:
        flash('The confirmation link is invalid or hax expired.')
    return redirect(url_for('.index'))