from datetime import datetime
from flask import Blueprint,render_template,url_for,redirect,session,request

mod = Blueprint('cms',__name__)

@mod.route('/')
def index():
    return render_template('index.html')
    
@mod.route('/cms/')
def cms_index():
    return render_template('cms/index.html')
    
@mod.route('/cms/pages')
def pages():
    return render_template('cms/pages.html')

@mod.route('/cms/posts')
def posts():
    return render_template('cms/posts.html')

@mod.route('/cms/users')
def users():
    return render_template('cms/users.html')

    
