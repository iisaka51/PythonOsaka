from tinydb import TinyDB, Query

db = TinyDB('db.json')

fruit = Query()
v1 = db.search(fruit.type == 'peach')
v2 = db.search(fruit.count > 5 )

# print(v1)
# print(v2)
