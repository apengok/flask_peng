import os
from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from config import config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object(config[os.getenv('FLASK_CONFIG') or 'default'])

bootstrap = Bootstrap()
bootstrap.init_app(app)

mail = Mail()
mail.init_app(app)

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.session_protection='strong'
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

moment = Moment()
moment.init_app(app)

admin = Admin(base_template='layout.html',template_mode='bootstrap3')
admin.init_app(app)


from apps.models import Users,BlogPost,Category
from apps.views import cmss,blogs,auths

app.register_blueprint(auths.mod)
app.register_blueprint(blogs.mod)
app.register_blueprint(cmss.mod)


from flask_admin.contrib.sqla import ModelView
from apps.views.adminview import PostBlogModelView,UserAdmin
admin.add_view(PostBlogModelView(BlogPost, db.session))
admin.add_view(UserAdmin(Users,db.session))
#admin.add_view(ModelView(Category, db.session))

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    bootstrap.init_app(app)
    db.init_app(app)
    
    login_manager.init_app(app)
    
    #blueprints
    from cms import cms as cms_blueprint
    app.register_blueprint(cms_blueprint)
    
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint)
    
    return app

