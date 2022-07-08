from tinydb_setup import *
from tinydb.operations import delete

database_initialized()

v1 = db.all()
v2 = db.update({'foo': 'bar'})

v3 = db.update(delete('foo'), user.name == 'Brian')
v4 = db.all()

# pprint(v1)
# pprint(v2)
# pprint(v3)
# pprint(v4)
