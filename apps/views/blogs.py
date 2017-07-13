from flask import Blueprint,render_template,redirect,url_for

mod = Blueprint('blog',__name__)

@mod.route('/blog/',methods=['GET','POST'])
def index():
    return render_template('blog/index.html')

