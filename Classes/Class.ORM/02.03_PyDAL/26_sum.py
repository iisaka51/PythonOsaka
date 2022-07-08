from logdb import *

v1 = db.log.severity.sum()
v2 = db().select(v1).first()[v1]

v3 = db.log.severity.max()
v4 = db().select(v3).first()[v3]

v5 = db(db.log.event.len() > 13).select()

# print(v1)
# ...
# print(v5)

