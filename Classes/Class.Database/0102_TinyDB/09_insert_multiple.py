from tinydb import TinyDB, Query
from user_data import user_data

db = TinyDB('users.json')

db.insert_multiple(user_data)
