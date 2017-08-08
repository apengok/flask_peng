from apps import db
from sqlalchemy import Column,ForeignKey,String,Integer,Table,Text
from sqlalchemy.orm import relationship
from datetime import datetime
from auths import Users



reltags = db.Table('reltags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('page_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
)

    
class BlogPost(db.Model):
    __tablename__ = 'posts'
    
    id = Column(Integer,primary_key=True)
    headline = Column(String(255), nullable=False)
    body = Column(Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
        backref=db.backref('posts', lazy='dynamic'))

    
    # many to many BlogPost<->Keyword
    tags = db.relationship('Tag', secondary=reltags, lazy='subquery',
        backref=db.backref('pages', lazy='dynamic'))
    
    
    comments = relationship('Comments',backref='posts',lazy='dynamic')                                
                           
    
    # def __init__(self,headline,body,author):
        # self.author = author
        # self.headline = headline
        # self.body = body
        
    def __repr__(self):
        return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    # def __init__(self, name):
        # self.name = name
        

    def __repr__(self):
        return '<Category %r>' % self.name




class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)        
    keyword = db.Column(db.String(50))
    
    # def __init__(self,name):
        # self.name = name
        
    def __repr__(self):
        return '<Category %r>' % self.keyword


class Comments(db.Model):
    __tablename__ = 'comments'
    
    id = Column(Integer,primary_key=True)
    guest = Column(String(50))
    body = Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = Column(Integer,db.ForeignKey('posts.id'))
    
    def __repr__(self):
        return "Comment(%r,%r)" %(self.guest,self.body)