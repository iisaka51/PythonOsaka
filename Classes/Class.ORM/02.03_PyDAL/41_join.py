from one_relationdb import *

v1 = db(db.person.id == db.car.owner_id).select()

v2 = db(db.person).select(join=db.car.on(db.person.id == db.car.owner_id))

def func(data):
    for d in data:
        print(f'{d.person.name} has {d.car.name}')

# print(v1)
# func(v1)
# print(v2)
# func(v2)

