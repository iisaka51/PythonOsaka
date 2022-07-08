import os
from tinydb import TinyDB, Query, where
from pprint import pprint
from user_data import user_data

DB_NAME='users.json'

db = TinyDB(DB_NAME)
user = Query()

def database_initialized():
    global db
    db.truncate()
    db.insert_multiple(user_data)

