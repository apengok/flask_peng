from flask import Blueprint,render_template,redirect,url_for,request
from flask_login import login_required,current_user
from apps import db
from apps.forms.blogs import PostBlogForm
from apps.models import Users,Role,BlogPost,Keyword

mod = Blueprint('blog',__name__)

@mod.route('/blog/',methods=['GET','POST'])
def index():
    page = request.args.get('page',1,type=int)
    pagination = current_user.posts.order_by(BlogPost.timestamp.desc()).paginate(
            page,per_page=1,error_out=False
        )
    blogs =pagination.items
    #blogs = current_user.posts.order_by(BlogPost.timestamp.desc()).all()
    return render_template('blog/index.html',blogs=blogs,pagination=pagination)
    
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
        post.keywords.append(Keyword(tags))
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('blog.index'))
    print 'invalid submit?'
    return render_template('blog/new_blog.html',form=form)

