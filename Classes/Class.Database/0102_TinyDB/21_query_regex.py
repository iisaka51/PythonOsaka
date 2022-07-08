from tinydb_setup import *

v1 = user.name.matches('[A-E][aZ]*')
v2 = db.search(user.name.matches('[A-E][aZ]*'))

# pprint(v1)
# pprint(v2)
