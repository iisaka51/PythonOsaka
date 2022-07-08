from tinydb import TinyDB, where

db = TinyDB('users.json')

data = {
    { 'name': 'John','
      'birthday': {'year': 1951, 'month': 8, 'day': 19},
      'country-code': 'GB' },
    { 'name': 'Freddie','
      'birthday': {'year': 1946, 'month': 9, 'day': 5},
      'country-code': 'GB' },
    { 'name': 'Brian','
      'birthday': {'year': 1947, 'month': 7, 'day': 19},
    { 'name': 'Roger','
      'birthday': {'year': 1949, 'month': 7, 'day': 26},

user = Query()
v1 = user.name.exists()

v1 = db.search(user.name.exists())
