from models import session, User

userList=[
  User(name='wendy', fullname='Wendy Williams', nickname='windy'),
  User(name='mary', fullname='Mary Contrary', nickname='mary'),
  User(name='fred', fullname='Fred Flintstone', nickname='freddy')
]

session.add_all(userList)
session.commit()
