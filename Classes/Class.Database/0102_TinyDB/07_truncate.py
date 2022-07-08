from tinydb import TinyDB

db = TinyDB('db.json')
v1 = db.truncate()
v2 = db.all()

# print(v1)
# print(v2)
