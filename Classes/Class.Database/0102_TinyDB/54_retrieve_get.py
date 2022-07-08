from tinydb_setup import *

v1 = db.get(user.name == 'John')
v2 = db.get(user.name == 'Jack')

# pprint(v1)
# pprint(v2)
