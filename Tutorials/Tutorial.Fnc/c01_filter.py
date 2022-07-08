import fnc
from users import users

v1 = fnc.filter({'active': True}, users)
v2 = list(v1)

# v1
# v2
