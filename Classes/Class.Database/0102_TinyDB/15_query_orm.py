from tinydb_setup import *

v1 = db.all()
v2 = db.search(user.name == 'John')
v3 = db.search(user.name == 'Jack')

# pprint(v1)
# pprint(v2)
# pprint(v3)
