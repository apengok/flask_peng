from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from config import config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection='strong'
login_manager.login_view = 'auth.login'


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
