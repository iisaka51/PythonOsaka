import dataset

db = dataset.connect('sqlite:///:memory:')

table = db['users']
table.insert(dict(name='Jack Bauer', age=55))
v1 = table.find_one(name='Jack Bauer')

table.insert(dict(name='Jack Bauer', age=55, belongs='CTU'))
v2 = table.find_one(name='Jack Bauer')

# print(v1)
# print(v2)
