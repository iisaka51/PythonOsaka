from tinydb_usersetup import *

v = db.search((user.name == 'John') | (user.name == 'Brian'))

# pprint(v)
