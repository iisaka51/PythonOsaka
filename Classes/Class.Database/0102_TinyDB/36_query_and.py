from tinydb_usersetup import *

v = db.search((user.name == 'Freddie') & (user.group.any(['user'])))

# pprint(v)
