from datetime import datetime
from flask import render_template,url_for,redirect,session,request,flash
from flask_login import login_user,logout_user,login_required
from . import auth
from .forms import RegistrationForm,LoginForm
#from .. import db
from apps.database import db_session
from .. models import Users


@auth.route('/auth/')
def index():
    return render_template('index.html')

@auth.route('/auth/login/',methods=['GET','POST'])
def login():
    form = LoginForm()
    print 'login?',request.method,form.email.data,form.password.data,form.remember_me.data
    print form.errors
    if form.validate_on_submit():
        print 'form submit'
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('blog.index'))
        flash('Invalid username or password.')
        
    return render_template('auth/login.html',form=form)

    
@auth.route('/auth/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('cms.index'))

@auth.route('/auth/register/',methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    
    if request.method == 'POST' and form.validate():
        user = Users(username=form.username.data, password=form.password.data,email=form.email.data,
        )
        
        db_session.add(user)
        db_session.commit()
        flash('Thanks for registering')
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)