from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path

data_dir = 'sampledb'
Path(data_dir).mkdir(exist_ok=True)

DSN = f'sqlite:///{data_dir}/account.sqlite'

engine = create_engine(DSN)
Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    fullname = Column(String)
    password = Column(String)
    about_me = Column(Text)

    def __repr__(self):
       return "<User('name={}', fullname={}, nickname={})>".format(
                     self.name, self.fullname, self.nickname)

Base.metadata.create_all(engine)
