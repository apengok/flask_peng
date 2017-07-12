from apps import db
from sqlalchemy import Column,ForeignKey,String,Integer,Table,Text
from sqlalchemy.orm import relationship
from auths import Users

post_keywords = Table('post_keywords',db.Model.metadata,
        Column('post_id',ForeignKey('posts.id'),primary_key=True),
        Column('keyword_id',ForeignKey('keywords.id'),primary_key=True)
    )
    
    
class BlogPost(db.Model):
    __tablename__ = 'posts'
    
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    headline = Column(String(255), nullable=False)
    body = Column(Text)
    
    # many to many BlogPost<->Keyword
    keywords = relationship('Keyword',
                           secondary=post_keywords,
                           back_populates='posts')
                           
    
    def __init__(self,headline,body,author):
        self.author = author
        self.headline = headline
        self.body = body
        
    def __repr__(self):
        return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)
        
        
class Keyword(db.Model):
    __tablename__ = 'keywords'
    
    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)
    posts = relationship('BlogPost',
                secondary=post_keywords,
                back_populates='keywords')
                
    def __init__(self,keyword):
        self.keyword = keyword
        
BlogPost.author = relationship(Users,back_populates="posts")
Users.posts = relationship(BlogPost,back_populates="author",lazy="dynamic")