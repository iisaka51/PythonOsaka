from tinydb_usersetup import *

v = db.search(user.name.one_of(['Jack', 'John']))

# pprint(v)
