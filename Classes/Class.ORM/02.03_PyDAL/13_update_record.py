from testdb import *

jack = person(name='Jack Bauer')
v1 = f'{jack}'
v2 = jack.copy()
v3 = jack.update_record(belongs="Dangerous Man")
v4 = person(name='Jack Bauer')

# print(v1)
# print(jack)
# print(v2)
# print(v3)
# print(v4)
