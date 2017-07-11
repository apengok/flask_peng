#from apps import db
from apps.database import Model
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(UserMixin,Model):
    __tablename__ = 'users'
    id = db.Column('id',db.Integer,primary_key=True)
    username = db.Column('username',db.String(64),unique=True)
    password_hash = db.Column(db.String(128))
    gender = db.Column('gender',db.String(64))
    email = db.Column('email',db.String(64),unique=True,index=True)
    
        
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)