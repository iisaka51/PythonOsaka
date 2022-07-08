from testdb import *

query = db.person.name != 'Jack Bauer'
q1 = f'{query}'
v1 = db(query).select()

query &= db.person.id > 3
q2 = f'{query}'
v2 = db(query).select()

query |= db.person.name == 'Ann Wilson'
q3 = f'{query}'
v3 = db(query).select()

# print(q1, v1)
# print(q2, v2)
# print(q3, v3)
