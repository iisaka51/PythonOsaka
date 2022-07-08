import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

db_engine = sa.create_engine('sqlite:///todo.db')

Session = sessionmaker(autocommit=False,
                        autoflush=False,
                        bind=db_engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

