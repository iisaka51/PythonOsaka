from testdb import *

Person._connection.debug = True

v1 = Person.selectBy(firstName="John", lastName="Doe")

# print(v1)
