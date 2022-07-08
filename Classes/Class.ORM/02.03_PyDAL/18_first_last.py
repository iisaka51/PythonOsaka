from testdb import *

rows = db().select(db.person.ALL)

v1 = rows.first()
v2 = rows.last()

# print(rows)
# print(v1)
# print(v2)
