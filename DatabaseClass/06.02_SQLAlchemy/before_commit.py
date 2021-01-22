from sqlalchemy import create_engine
engine = create_engine('sqlite:///test.db')
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
       return "<User('name={}', fullname={}, nickname={})>".format(
                     self.name, self.fullname, self.nickname)
Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')

session.add(ed_user)
users = session.query(User)

ed = users.filter_by(name='ed').first()
userList=[
  User(name='wendy', fullname='Wendy Williams', nickname='windy'),
  User(name='mary', fullname='Mary Contrary', nickname='mary'),
  User(name='fred', fullname='Fred Flintstone', nickname='freddy')
]

session.add_all(userList)
ed_user.nickname = 'eddie'
session.dirty
session.new
