from tinydb_usersetup import *

v1 = db.search(user.group.any(['user']))
v2 = db.search(user.group.any(['operator']))
v3 = db.search(user.group.any(['operator', 'admin']))

# pprint(v1)
# pprint(v2)
# pprint(v3)
