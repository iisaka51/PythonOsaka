from tinydb_setup import *

v1 = user.name.matches('B+')
v2 = db.search(user.name.matches('B+'))

# pprint(v1)
# pprint(v2)
