from testdb import *

v1 = db(db.person).select(limitby=(2, 5))

def func(data):
    for p in data:
        print(f'{p.id} {p.name} {p.age} {p.belongs}')

# func(v1)
# db.close()

