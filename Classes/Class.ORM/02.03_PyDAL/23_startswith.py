from testdb import *

v1 = db(db.person.name.startswith('David')).select()
v2 = db(db.person.name.endswith('Wilson')).select()
v3 = db(db.person.name.contains('An')).select()
v4 = db(db.person.name.contains(['Ann', 'David'])).select()
v5 = db(db.person.name.contains(['Ann', 'David'], all=False)).select()
v6 = db(db.person.name.contains(['Ann', 'David'], all=True)).select()

condition = db.person.belongs.contains('CTU')
yes_no = condition.case('Yes','No')
v7 = db().select(db.person.name, yes_no)

# print(v1)
# ...
# print(v7)
# func(v7)
