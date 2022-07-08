from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///account.db')
Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    fullname = Column(String(32))
    password = Column(String(256))
    about_you = Column(String(256))

    def __repr__(self):
       return "<User('username={}', fullname={})>".format(
                     self.username, self.fullname)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
