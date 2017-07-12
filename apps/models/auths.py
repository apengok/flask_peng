from apps import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from sqlalchemy import Column,Integer,String
from apps import login_manager

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(UserMixin,db.Model):
    __tablename__ = 'users'
    id = Column('id',Integer,primary_key=True)
    username = Column('username',String(64),unique=True)
    password_hash = Column(String(128))
    gender = Column('gender',String(64))
    email = Column('email',String(64),unique=True,index=True)
    cell_phone = Column('cell_phone',String(11))
    
        
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)