from tinydb import TinyDB, Query

db = TinyDB('db.json')

fruit = Query()
v1 = db.search(fruit.type == 'apple')
doc_id = db.update({'count': 10}, fruit.type == 'apple')
v2 = db.search(fruit.type == 'apple')

# print(v1)
# print(doc_id)
# print(v2)
