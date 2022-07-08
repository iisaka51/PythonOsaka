import os
from pony import orm

DATABASE_NAME = 'user.sqlite'


db = orm.Database()
basedir = os.path.abspath(os.path.dirname(__file__))
db_file = basedir + '/' + DATABASE_NAME
db.bind(provider='sqlite', filename=db_file, create_db=True)

class User(db.Model):
     id = orm.Required(int, primary_key)
     username = orm.Required(str, uniq=True)
     email = orm.Required(str)
     password = orm.Required(str)

     def __repr__(self):
         return f'<User {self.username}>'
