from apps import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
from sqlalchemy import Column,Integer,String,Float
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,request
import hashlib



class WBalance(db.Model):
    __tablename__ = 'wbalance'
    id = Column('id',db.Integer,primary_key=True)
    name = Column('name',db.String(64),unique=True)
    totoal_in = Column(db.Float)
    auth_use = Column(db.Float)
    loss = Column(db.Float)
    charge_auth = Column(db.Float)
    uncharge_auth = Column(db.Float)
    charge_measure = Column(db.Float)
    charge_unmeasure = Column(db.Float)
    uncharge_measure = Column(db.Float)
    uncharge_unmeasure = Column(db.Float)
    apparent_loss = Column(db.Float)
    actual_loss = Column(db.Float)
    unauth_use = Column(db.Float)
    statistic_error = Column(db.Float)
    money_back = Column(db.Float)
    money_waste = Column(db.Float)
    
    
    def __str__(self):
        return u'%s wbalance' % self.name
    

