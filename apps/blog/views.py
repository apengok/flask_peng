from flask import render_template,redirect,url_for

from . import blog

@blog.route('/')
@blog.route('/blog/',methods=['GET','POST'])
def index():
    return render_template('blog/index.html')

