from testdb import *

# v1 = db(db.person).select(distinct = db.person.name[:4])
# SyntaxError: DISTINCT ON is not supported by SQLite

v1 = db(db.person).select(db.person.name[:4])

# print(v1)
