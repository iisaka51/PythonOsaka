from testdb import *
from pprint import pprint

SQL = 'SELECT * FROM person;'
v1 = db.executesql(SQL)

# pprint(v1)
