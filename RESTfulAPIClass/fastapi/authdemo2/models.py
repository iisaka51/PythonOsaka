import databases
import sqlalchemy
from fastapi_users import FastAPIUsers, models
from fastapi_users.db import (
        sqlalchemy, SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
    )
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from db import Base, database

class User(models.BaseUser):
    pass

class UserCreate(User, models.BaseUserCreate):
    pass

class UserUpdate(User, models.BaseUserUpdate):
    pass

class UserDB(User, models.BaseUserDB):
    pass

class UserTable(Base, SQLAlchemyBaseUserTable):
    pass

users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)
