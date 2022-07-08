from tinydb_usersetup import *

v = db.search(~ (user.name == 'Freddie'))

# pprint(v)
