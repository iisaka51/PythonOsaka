from zodb_mydata import *

v1 = root.members
v2 = root.members[0].getName()

connection.close()

# print(v1)
# print(v2)

