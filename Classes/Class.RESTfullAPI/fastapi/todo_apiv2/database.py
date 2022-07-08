import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from models import Base

engine = sa.create_engine('sqlite:///todo.db')

Session = sessionmaker(autocommit=False,
                        autoflush=False,
                        bind=engine)
