from testdb import *

id1 = person.update_or_insert(db.person.name == 'David Palmer',
                              name='David Palmer',
                              age=55, belongs='Democratic Senator')
v1 = db(person).select(person.ALL)

id2 = person.update_or_insert(db.person.name == 'David Palmer',
                              name='David Palmer',
                              age=55, belongs='White House')
v2 = db(person).select(person.ALL)

# print(id1)
# print(v1)
# print(id2)
# print(v2)
