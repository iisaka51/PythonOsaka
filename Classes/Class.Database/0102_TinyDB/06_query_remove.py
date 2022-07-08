from tinydb import TinyDB, Query

db = TinyDB('db.json')

fruit = Query()
id1 = db.remove(fruit.count < 5)
v1 = db.all()
id2 = db.remove(fruit.count > 20)
v2 = db.all()

# print(id1)
# print(v1)
# print(id2)
# print(v2)
