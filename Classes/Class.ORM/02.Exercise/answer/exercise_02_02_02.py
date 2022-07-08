from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import URLType
from furl import furl
from pathlib import Path

data_dir = 'sampledb'
Path(data_dir).mkdir(exist_ok=True)

DSN = f'sqlite:///{data_dir}/moviedb.sqlite'

engine = create_engine(DSN)
Base = declarative_base()

class Movie(Base():
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    year = Column(Integer)
    def __repr__(self):
       return "<Movie('id={id}', title={title}, year={year})>>"

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    birthday = Column(Date)
    imdb = Column(URLType)
    movies = Column(ForignKeyField)

    def __repr__(self):
       return "<User('name={}', fullname={}, nickname={})>".format(
                     self.name, self.fullname, self.nickname)

Base.metadata.create_all(engine)
