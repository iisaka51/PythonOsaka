from logdb import *

v1 = db().select(db.log.ALL)
v2 = db(db.log.event_time.year() > 2018).select()

# print(v1)
# print(v2)
