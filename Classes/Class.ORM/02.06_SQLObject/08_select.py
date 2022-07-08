from testdb import *

Person._connection.debug = True

v1 = Person.select(Person.q.firstName=="John")
v2 = list(v1)

# print(v1)
# print(v2)
