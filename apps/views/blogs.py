from flask import Blueprint,render_template,redirect,url_for,request
from flask_login import login_required,current_user
from apps import db
from apps.forms.blogs import PostBlogForm,CommentForm
from apps.models import Users,Role,BlogPost,Keyword,Comments

mod = Blueprint('blog',__name__)

@mod.route('/blog/',methods=['GET','POST'])
def index():
    page = request.args.get('page',1,type=int)
    # pagination = current_user.posts.order_by(BlogPost.timestamp.desc()).paginate(
            # page,per_page=20,error_out=False
        # )
    #blogs =pagination.items
    blogs = BlogPost.query.order_by(BlogPost.timestamp.desc()).all()
    return render_template('blog/index.html',blogs=blogs,pagination=[])
    
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

@mod.route('/blog/<int:id>',methods=['GET','POST'])
def post(id):
    post = BlogPost.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        guest = form.guest.data
        body = form.body.data
        comment = Comments(guest=guest,post=post,body=body)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.post',id=post.id,page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / 20 + 1
    pagination = post.comments.order_by(Comments.timestamp.asc()).paginate(
    page, per_page=20,    error_out=False)
    comments = pagination.items
    return render_template('blog/post.html', posts=[post], form=form,
        comments=comments, pagination=pagination)
        