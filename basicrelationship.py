from sqlalchemy import Table, Column, Integer, ForeignKey,String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()

Base.metadata.create_all(engine)

#create session
Session = sessionmaker(bind=engine)
#or
# Session = sessionmaker()
# Session.configure(bind=engine)  # once engine is available
session = Session()



#one to many
#A one to many relationship places a foreign key on the child table referencing the parent. 
#relationship() is then specified on the parent, as referencing a collection of items represented by the child:
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child",backref='parent',lazy='dynamic')
    name = Column(String)
    
    def __repr__(self):
        return self.name

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey('parent.id'))

    def __repr__(self):
        return self.name
        
        
#Many to one        
#Many to one places a foreign key in the parent table referencing the child. 
#relationship() is declared on the parent, where a new scalar-holding attribute will be created: