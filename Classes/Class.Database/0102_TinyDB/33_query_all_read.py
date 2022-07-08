from tinydb_usersetup import *

q = group.permission.any(permission.type == 'read')
v = db_group.search(group.permission.all(permission.type == 'read'))

# pprint(q)
# pprint(v)
