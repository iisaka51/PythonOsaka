from tinydb_setup import *

adam = {
    'name': 'Adam',
    'birthday': {'year': 1982, 'month': 1, 'day': 29},
    'country-code': 'USA'
}

database_initialized()
v1 = db.all()
v2 = db.upsert(adam, user.name == 'Freddie')
v3 = db.all()

database_initialized()
v4 = db.upsert(adam, user.name == 'Adam')
v5 = db.all()

# pprint(v1)
# pprint(v2)
# pprint(v3)
# pprint(v4)
# pprint(v5)
