from datetime import datetime
from flask import render_template,url_for,redirect,session,request
from . import cms

@cms.route('/')
def index():
    return render_template('index.html')
    
@cms.route('/cms/')
def cms_index():
    return render_template('cms/index.html')
    
@cms.route('/cms/pages')
def pages():
    return render_template('cms/pages.html')

@cms.route('/cms/posts')
def posts():
    return render_template('cms/posts.html')

@cms.route('/cms/users')
def users():
    return render_template('cms/users.html')

    
