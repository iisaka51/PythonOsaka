from one_relation_db import *

Person._connection.debug = False

v1 = Person.select("""address.person_id = person.id AND
                         address.zip LIKE '504%'""",
                      clauseTables=['address'])

# print(v1)
