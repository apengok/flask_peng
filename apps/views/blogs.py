from flask import Blueprint,render_template,redirect,url_for
from flask_login import login_required

mod = Blueprint('blog',__name__)

@mod.route('/blog/',methods=['GET','POST'])
def index():
    return render_template('blog/index.html')
    
@mod.route('/blog/new_post',methods=['GET','POST'])
@login_required
def new_blog():
    return render_template('blog/new_blog.html')

