from testdb import *

v1 = db(db.person).select(orderby=db.person.age)
v2 = db(db.person).select(orderby=~db.person.age)

def func(data):
    for p in data:
        print(f'{p.id} {p.name} {p.age}')

# func(v1)
# func(v2)
# db.close()
