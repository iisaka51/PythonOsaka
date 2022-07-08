from testdb import *

p1 = Person.get(1)
v1 = p1.firstName
v2 = p1.middleInitial
p1.middleInitial = 'Q'
v3 = p1.middleInitial

p2 = Person.get(1)
v4 = p1 is p2

# print(v1)
# print(v2)
# print(p1)
# print(v3)
#
# print(p2)
# print(v4)
