from tinydb import TinyDB, Query
from user_data import user_data

db = TinyDB('users.json')

for p in user_data:
    db.insert(p)
