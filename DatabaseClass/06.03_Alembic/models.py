from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///test.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
#    password = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
       return "<User('name={}', fullname={}, nickname={})>".format(
                     self.name, self.fullname, self.nickname)

# Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
