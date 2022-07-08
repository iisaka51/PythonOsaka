import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
     __tablename__ = 'tasks'
     id = sa.Column(sa.Integer, primary_key = True)
     title = sa.Column(sa.String(32), index = True)
     description = sa.Column(sa.Text(128), nullable=True)
     done = sa.Column(sa.Boolean)
