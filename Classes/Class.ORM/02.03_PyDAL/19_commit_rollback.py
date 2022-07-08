from testdb import *

id1 = person.insert(name='David Palmer', age=55, belongs='Democratic Senator')
v1 = db(person).select(person.ALL)
v2 = db.rollback()
v3 = db(person).select(person.ALL)

id2 = person.insert(name='David Palmer', age=55, belongs='Democratic Senator')
v4 = db.commit()

from testdb import *
v5 = db(person).select(person.ALL)
david = person(name='David Palmer')
v6 = david.delete_record()
v7 = db.commit()


# print(id1)
# print(v1)
# ...
# print(v7)
