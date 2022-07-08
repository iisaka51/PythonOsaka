from testdb import *

v1 = db(db.person.name.regexp('A.*n')).select()
v2 = db(db.person.name.regexp('A.*n$')).select()

# print(v1)
# print(v2)
