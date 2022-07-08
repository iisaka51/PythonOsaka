from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path

data_dir = 'sampledb'
Path(data_dir).mkdir(exist_ok=True)

DSN = f'sqlite:///{data_dir}/account.sqlite'

engine = create_engine(DSN)
Base = declarative_base()

class Account(Base):
    # ...

    def __repr__(self):
       return "<User(f'id={id}, username={username}', fullname={fullname}, password={password})>")

