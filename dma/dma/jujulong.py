# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Catalog(Base):
    __tablename__ = 'catalog'

    id = Column(Integer, primary_key=True, server_default=text("nextval('catalog_id_seq'::regclass)"))
    cloth = Column(String(10))
    color_id = Column(ForeignKey(u'colors.id'))
    size = Column(String(10))
    totoal = Column(Integer)
    coming = Column(Integer)
    sale = Column(Integer)
    receved = Column(Integer)
    storge = Column(Integer)
    left = Column(Integer)
    diff = Column(Integer)

    color = relationship(u'Color')


class Color(Base):
    __tablename__ = 'colors'

    id = Column(Integer, primary_key=True, server_default=text("nextval('colors_id_seq'::regclass)"))
    name = Column(String(10), unique=True)
    style_id = Column(ForeignKey(u'styles.id'))

    style = relationship(u'Style')


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, server_default=text("nextval('comments_id_seq'::regclass)"))
    body = Column(Text)
    body_html = Column(Text)
    timestamp = Column(DateTime, index=True)
    disabled = Column(Boolean)
    author_id = Column(ForeignKey(u'users.id'))
    post_id = Column(ForeignKey(u'posts.id'))

    author = relationship(u'User')
    post = relationship(u'Post')


class Follow(Base):
    __tablename__ = 'follows'

    follower_id = Column(ForeignKey(u'users.id'), primary_key=True, nullable=False)
    followed_id = Column(ForeignKey(u'users.id'), primary_key=True, nullable=False)
    timestamp = Column(DateTime)

    followed = relationship(u'User', primaryjoin='Follow.followed_id == User.id')
    follower = relationship(u'User', primaryjoin='Follow.follower_id == User.id')


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, server_default=text("nextval('posts_id_seq'::regclass)"))
    body = Column(Text)
    body_html = Column(Text)
    timestamp = Column(DateTime, index=True)
    author_id = Column(ForeignKey(u'users.id'))

    author = relationship(u'User')


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, server_default=text("nextval('roles_id_seq'::regclass)"))
    name = Column(String(64), unique=True)
    default = Column(Boolean, index=True)
    permissions = Column(Integer)


class Style(Base):
    __tablename__ = 'styles'

    id = Column(Integer, primary_key=True, server_default=text("nextval('styles_id_seq'::regclass)"))
    name = Column(String(10), unique=True)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, server_default=text("nextval('users_id_seq'::regclass)"))
    email = Column(String(120), unique=True)
    username = Column(String(64), unique=True)
    role_id = Column(ForeignKey(u'roles.id'))
    password_hash = Column(String(128))
    confirmed = Column(Boolean)
    name = Column(String(64))
    location = Column(String(64))
    about_me = Column(Text)
    member_since = Column(DateTime)
    last_seen = Column(DateTime)
    avatar_hash = Column(String(32))

    role = relationship(u'Role')
