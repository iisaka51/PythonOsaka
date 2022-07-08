from tinydb_setup import *

v1 = db.contains(user.name == 'John')
v2 = v1 and db.search(user.name == 'John')[0] or None

v3 = db.contains(user.name == 'Jack')
v4 = v3 and db.search(user.name == 'Jack')[0] or None

# print(v1, v2)
# print(v3, v4)

