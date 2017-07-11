from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker,backref,relation
from sqlalchemy.ext.declarative import declarative_base

from apps import app

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
        convert_unicode=True,
        **app.config['DATABASE_CONNECT_OPTIONS'])
        
db_session = scoped_session(sessionmaker(autocommit=False,
        autoflush=False,
        bind=engine))
        
def init_db():
    from apps.models import Users
    from apps.models.blogs import BlogPost,Keyword
    Model.metadata.create_all(bind=engine)
    
Model = declarative_base(name='Model')
Model.query = db_session.query_property()