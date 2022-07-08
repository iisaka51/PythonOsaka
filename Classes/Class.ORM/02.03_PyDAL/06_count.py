from testdb import *

v1 = db().select(db.person.ALL)
v2 = db(db.person.id).count()

# print(v1)
# print(v2)
# db.close()

