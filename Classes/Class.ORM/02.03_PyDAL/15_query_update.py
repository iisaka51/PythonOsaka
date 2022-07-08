from testdb import *

id1 = person.insert(name='David Palmer', age=55, belongs='Democratic Senator')
v1 = db(person).select(person.ALL)
david = person(name='David Palmer')
v2 = f'{david}'
v3 = david.copy()
v4 = db(person.belongs.like('D%')).update(belongs='White House')
v5 = db(person).select(person.ALL)

v6 = db(person.name.lower() == 'david palmer').delete()
v7 = db(person).select(person.ALL)

# print(id1)
# print(v1)
# print(david)
# print(v2)
# ...
# print(v7)
