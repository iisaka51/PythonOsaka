from tinydb_setup import *

database_initialized()

v1 = db.search(where('birthday').year == 1947)
v2 = db.search(where('birthday')['year'] == 1947)

# pprint(v1)
# pprint(v2)
