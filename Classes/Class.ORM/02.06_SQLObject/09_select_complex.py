from testdb import *

Person._connection.debug = True

v1 = Person.select(
                OR(Person.q.firstName == "John",
                LIKE(Person.q.lastName, "%Hope%")))
v2 = list(v1)

# print(v1)
# print(v2)
