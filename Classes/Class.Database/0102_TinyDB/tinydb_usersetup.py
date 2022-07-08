from tinydb import TinyDB, Query, where
from pprint import pprint
from user_auth_data import user_data, group_data

DB_NAME='usergroup.json'

db = TinyDB(DB_NAME)
db_group = db.table('group')

user = Query()
group = Query()
permission = Query()

def database_initialized():
    global db, db_group
    db.truncate()
    db_group.truncate()
    db.insert_multiple(user_data)
    db_group = db.table('group')
    db_group.insert_multiple(group_data)

