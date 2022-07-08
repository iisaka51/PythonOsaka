from one_relation_db import *

Person._connection.debug = False

p1 = Person.select(
        AND(Address.q.personID == Person.q.id,
            Address.q.zip.startswith('504')))
v1 = list(p1)

p2 = Person.select(
        AND(Address.q.personID == Person.q.id,
            Address.q.zip.startswith('554')))
v2 = list(p2)

# print(p1)
# print(v1)
# print(p2)
# print(v2)
