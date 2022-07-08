from testdb import *

v1 = db().select(db.person.ALL)

with open('testdata.csv', 'w') as f:
    v1.export_to_csv_file(f)

# print(v1)
# !cat testdata.csv
