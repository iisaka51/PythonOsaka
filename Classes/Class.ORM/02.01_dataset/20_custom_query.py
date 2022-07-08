from testdb import *

v1 = db.query('SELECT belongs, COUNT(*) c FROM users GROUP BY belongs')

def func(data):
    for row in data:
        print(row['belongs'], row['c'])

# print(v1)
# func(v1)
