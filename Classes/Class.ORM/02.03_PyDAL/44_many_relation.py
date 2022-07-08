from many_relationdb import *

d1 = db().select(db.person.ALL)
d2 = db().select(db.thing.ALL)
d3 = db().select(db.ownership.ALL)

v1 = db((db.person.id == db.ownership.person) &
        (db.thing.id == db.ownership.thing))

v2 = v1.select()
v3 = v1(db.person.name == 'Alex').select()
v4 = v1(db.thing.name == 'Boat').select()

def func(out_type, data):
    for d in data:
        if out_type == 1:   # all
            print(f'{d.person.name} has {d.thing.name}')
        elif out_type == 2: # thing
            print(f'{d.thing.name}')
        elif out_type == 3:   # person
            print(f'{d.person.name}')
        else:               # other
            print(f'{d.id}, {d.name}')

# print(v1)
# ...
# print(v4)
# func(1, v2)
# func(2, v3)
# func(3, v4)
