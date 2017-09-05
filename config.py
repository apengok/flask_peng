import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SUBJECT_PREFIX = '[Flasky]'
    MAIL_SENDER = 'Flasky Admin <peng.weilin@yahoo.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    PENG_ADMIN = os.environ.get('PENG_ADMIN') or 'peng.weilin@yahoo.com'
    
    MAIL_SERVER = 'smtp.mail.yahoo.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'peng.weilin@yahoo.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '57266713sweet'
    
    IMAGE_UPLOADS_DIR = os.path.join(basedir,'apps','static','images')
    
    @staticmethod
    def init_app(app):
        pass
        
class DevelopmentConfig(Config):
    DEBUG = True
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    DATABASE_CONNECT_OPTIONS = {}

    

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    DATABASE_CONNECT_OPTIONS = {}


    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    DATABASE_CONNECT_OPTIONS = {}



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}