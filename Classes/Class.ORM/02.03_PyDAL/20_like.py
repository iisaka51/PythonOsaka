from testdb import *

v1 = db(db.person.belongs.like('H%')).select()
v2 = db(db.person.belongs.like('h%', case_sensitive=False)).select()
v3 = db(db.person.belongs.ilike('h%')).select()

def func(data):
    for d in data:
        print(f'{d.name} {d.age} {d.belongs}')

# print(v1)
# print(v2)
# print(v3)
# func(v1)
# func(v2)
# func(v3)
