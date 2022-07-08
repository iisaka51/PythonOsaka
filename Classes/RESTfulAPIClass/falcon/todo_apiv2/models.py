import sqlalchemy as sa
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy.ext.declarative import declarative_base

db_engine = sa.create_engine('sqlite:///todo.db')
Base = declarative_base()

class Task(Base):
     __tablename__ = 'tasks'
     id = sa.Column(sa.Integer, primary_key = True)
     title = sa.Column(sa.String(128), index = True)
     description = sa.Column(sa.Text(256), nullable=True)
     done = sa.Column(sa.Boolean)

     def __init__(self, id=None, title='new task', description='', done=False):
        self.id = id
        self.title = title
        self.description = description
        self.done = done

     def __repr__(self):
         return f'<Task({self.id}, {self.title}, {self.description}, {self.done})>'
