from userdb import *

v1 = User(id=10, name='John Smith', friend_ids=[1, 2])

try:
    v2 = User(id='a', name=['John', 'Smith'], friend_ids=['a'])
    msg = ''
except TypeValidationError as e:
    v2 = None
    msg = e

# print(v1)
# print(v2)
# print(msg)
