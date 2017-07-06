from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from config import config

bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    bootstrap.init_app(app)
    
    from cms import cms as cms_blueprint
    app.register_blueprint(cms_blueprint)
    
    return app
