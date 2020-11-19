import sqlalchemy
import databases
from sqlalchemy.ext.declarative import declarative_base
from fastapi_users.db import SQLAlchemyUserDatabase

DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)
Base = declarative_base()

engine = sqlalchemy.create_engine(
             DATABASE_URL, connect_args={"check_same_thread": False}
         )
Base.metadata.create_all(engine)
