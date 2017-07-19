from datetime import datetime
from flask import Blueprint,render_template,url_for,redirect,session,request,flash
from flask_login import login_user,logout_user,login_required,current_user

from apps.forms.auths import RegistrationForm,LoginForm,ChangePasswordForm,\
PasswordResetRequestForm,ResetPasswordForm,ChangeEmailForm
#from .. import db
from apps import db
from apps.models import Users

from apps.email import send_email


mod = Blueprint('auth',__name__)


@mod.before_app_request
def before_requst():
    
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))
            
@mod.route('/user/<username>')
def user(username):
    user = Users.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html',user=user)
        

@mod.route('/auth/unconfirmed/')
def unconfirmed():
    print 'unconfirmed?'
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('/')
    
    return render_template('auth/unconfirmed.html')
    
@mod.route('/auth/confirm/')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,'Confirm you account',
            '/auth/email/confirm',user=current_user,token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('.index'))
        
@mod.route('/auth/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account.Thanks!')
    else:
        flash('The confirmation link is invalid or hax expired.')
    return redirect(url_for('.index'))        

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
    
@mod.route('/auth/change_password/',methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('You password has been updated.')
            return redirect(url_for('auth.index'))
        else:
            flash('Invalid password.')
    return render_template('auth/change_password.html',form=form)
    
@mod.route('/auth/reset_password/',methods=['GET','POST'])
def reset_password_request():
    
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email,'Reset you Password',
            '/auth/email/reset_password',user=user,token=token,
            next=request.args.get('next'))
            flash('An email with instructions to rest your password has been sent to you.')
            return redirect(url_for('auth.login'))
        else:
            print 'user is None?'
            flash('This email not registered.')
    return render_template('auth/reset_password.html',form=form)
    
@mod.route('/auth/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('auth.index'))
        if user.reset_password(token,form.password.data):
            flash('You password has been reset.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('auth.index'))
        
    return render_template('auth/reset_password.html',form=form)

    
@mod.route('/auth/change_email/',methods=['GET','POST'])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        current_user.email = form.password.email
        db.session.add(current_user)
        db.session.commit()
        flash('You email has been updated.')
        return redirect(url_for('auth.index'))
    
    return render_template('auth/change_email/',form=form)