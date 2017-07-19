from apps import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
from sqlalchemy import Column,Integer,String
from apps import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,request
import hashlib

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80
    
class Role(db.Model):
    __tablename__ = 'roles'
    id = Column('id',db.Integer,primary_key=True)
    name = Column('name',db.String(64),unique=True)
    default = Column(db.Boolean,default=False,index=True)
    permissions = Column(db.Integer)
    users = db.relationship('Users',backref='role',lazy='dynamic')
    
    @staticmethod
    def insert_roles():
        roles = {
            'User':(Permission.FOLLOW |
                    Permission.COMMENT |
                    Permission.WRITE_ARTICLES,True),
            'Moderator':(Permission.FOLLOW |
                        Permission.COMMENT |
                        Permission.WRITE_ARTICLES |
                        Permission.MODERATE_COMMENTS,False),
            'Administrator':(0xff,False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()
        
class Users(UserMixin,db.Model):
    __tablename__ = 'users'
    id = Column('id',Integer,primary_key=True)
    username = Column('username',String(64),unique=True)
    password_hash = Column(String(128))
    gender = Column('gender',String(64))
    email = Column('email',String(64),unique=True,index=True)
    confirmed = Column('confirmed',db.Boolean,default=False)
    role_id = Column(db.Integer,db.ForeignKey('roles.id'))
    
    def __init__(self,**kwargs):
        super(Users,self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['PENG_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        
        
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
        
    def generate_confirmation_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})
    
    def generate_reset_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'reset':self.id})
        
    def reset_password(self,token,new_password):
        s =  Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True
        
    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True
        
    def gravatar(self,size=100,default='identicon',rating='g'):
        if request.is_secure:
            url = 'https://www.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = hashlib.md5('peng.weilin@yahoo.com'.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
        url=url,hash=hash,size=size,default=default,rating=rating)