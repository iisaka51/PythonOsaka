from university1 import *

sql_debug(True)
v1 = select(g for g in Group if max(g.students.gpa) < 4)
v2 = select(g for g in Group if JOIN(max(g.students.gpa) < 4))

# print(v1)
# print(v2)
# print(v1.first())
# print(v2.first())
