from one_relationdb import *


v1 = db().select(db.person.ALL, db.car.ALL,
                 left=db.car.on(db.person.id == db.car.owner_id))

def func(data):
    for d in data:
        print(f'{d.person.name} has {d.car.name}')

# print(v1)
# func(v1)

