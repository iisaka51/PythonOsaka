from testdb import *

rows = db().select(db.person.ALL)

def func(data):
    for row in data:
        print(f'{row.id}, {row.name}, {row.age}, {row.belongs}')

# print(rows)
# func(rows)
