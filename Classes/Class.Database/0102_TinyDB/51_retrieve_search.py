from tinydb_setup import *

v1 = db.search(user.name == 'John')

try:
    v2 = db.search(user.name == 'Jack')[0]
except IndexError:
    v2 = None

# print(v1)
# print(v2)

