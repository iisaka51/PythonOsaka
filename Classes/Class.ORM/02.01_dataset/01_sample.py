import dataset

db = dataset.connect('sqlite:///:memory:')

table = db['users']
table.insert(dict(name='Jack Bauer', age=55))
# table.insert(dict(name='Jack Bauer', age=55, belongs='CTU'))
table.insert(dict(name='David Gilmour', age=75, belongs='PinkFloyd'))

jack = table.find_one(name='Jack Bauer')

# print(jack)
