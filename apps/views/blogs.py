from flask import Blueprint,render_template,redirect,url_for
from flask_login import login_required,current_user
from apps import db
from apps.forms.blogs import PostBlogForm
from apps.models import Users,Role,BlogPost,Keyword

mod = Blueprint('blog',__name__)

@mod.route('/blog/',methods=['GET','POST'])
def index():
    blogs = current_user.posts.order_by(BlogPost.timestamp.desc()).all()
    return render_template('blog/index.html',blogs=blogs)
    
@mod.route('/blog/new_blog/',methods=['GET','POST'])
@login_required
def new_blog():
    form = PostBlogForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        publish = form.publish.data
        tags = form.tags.data
        description = form.description.data
        
        post = BlogPost(headline=title,body=body,author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('blog.index'))
    return render_template('blog/new_blog.html',form=form)

