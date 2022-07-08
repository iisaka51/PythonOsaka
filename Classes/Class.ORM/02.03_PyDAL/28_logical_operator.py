from testdb import *

v1 = db((db.person.belongs == 'CTU') & (db.person.id >= 2)).select()
v2 = db((db.person.name == 'David Gilmour') | (db.person.id == 5)).select()
v3 = db((db.person.name != 'David Gilmour') | (db.person.id > 3)).select()
v4 = db(~(db.person.name == 'Jack Bauer') | (db.person.id > 3)).select()

# print(v1)
# ...
# print(v4)
