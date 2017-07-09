from apps import db
from werkzeug.security import generate_password_hash,check_password_hash

class Users(db.Model):
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
        self.password_hash = generated_password_hash(password)
        
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)