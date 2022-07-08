from one_relationdb import *

count = db.person.id.count()
v1 = db(db.person.id == db.car.owner_id).select(
                            db.person.name, count, groupby=db.person.name)

def func(data):
    for d in data:
        print(f'{d.person.name} has {d[count]} cars')

# print(v1)
# func(v1)
