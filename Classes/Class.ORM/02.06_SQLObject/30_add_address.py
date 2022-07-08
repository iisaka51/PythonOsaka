from one_relation_db import *

p = Person.get(1)
v1 = p.address
v2 = Address(street='123 W Main St', city='Smallsville',
             state='MN', zip='55407', person=p)

v3 = p.address

# print(p)
# print(v1)
# print(v2)
# print(v3)
