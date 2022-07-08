from testdb import *

v1 = db().select(db.person.ALL)

with open('testdata.csv', 'rb') as f:
    db.person.import_from_csv_file(f)

v2 = db().select(db.person.ALL)

# print(v1)
# print(v2)
