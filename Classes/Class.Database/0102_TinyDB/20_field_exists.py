from tinydb_setup import *

v1 = user.name.exists()
v2 = db.search(user.name.exists())

# pprint(v1)
# pprint(v2)
