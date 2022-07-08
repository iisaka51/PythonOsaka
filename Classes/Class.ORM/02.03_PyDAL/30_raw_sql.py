from testdb import *

v1 = db.person._insert(name='Alex')
v2 = db(db.person.name == 'Alex')._count()
v3 = db(db.person.name == 'Alex')._select()
v4 = db(db.person.name == 'Alex')._delete()
v5 = db(db.person.name == 'Alex')._update(name='Susan')

# print(v1)
# ...
# print(v5)
