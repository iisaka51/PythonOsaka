import dataset

db = dataset.connect('sqlite:///:memory:')

table = db['users']
table.insert(dict(name='Jack Bauer', age=55))
v1 = table.find_one(name='Jack Bauer')

table.insert(dict(name='David Gilmour', age=75, belongs='PinkFloyd'))
v2 = table.find_one(name='David Gilmour')
v3 = table.find_one(name='Jack Bauer')

# print(v1)
# print(v2)
# print(v3)
