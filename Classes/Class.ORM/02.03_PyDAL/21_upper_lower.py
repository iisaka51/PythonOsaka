from testdb import *

v1 = db(db.person.name.upper().like('DAVID%')).select()
v2 = db(db.person.name.lower().like('david%')).select()

# print(v1)
# print(v2)
