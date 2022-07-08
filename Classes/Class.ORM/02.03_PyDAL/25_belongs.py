from logdb import *

v1 = db(db.log.severity.belongs((1, 2))).select()
v2 = db(db.log.severity == 3)._select(db.log.event_time)
v3 = db(db.log.event_time.belongs(v2)).select()

def func(data):
    for d in data:
        print(d.severity, d.event)

# print(v1)
# print(v2)
# print(v3)
# func(v3)
