from testdb import *

Person._connection.debug = True

v1 = Person.select("""person.first_name = 'John' AND
                             person.last_name LIKE 'D%'""")
v2 = list(v1)

# print(v1)
# print(v2)
