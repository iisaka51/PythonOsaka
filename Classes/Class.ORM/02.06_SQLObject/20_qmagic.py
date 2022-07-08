from testdb import *

Person._connection.debug = True

v1 = Person.select(Person.q.firstName=="John")

# print(v1)
