from university1 import *

sql_debug(True)
v1 = left_join((g, count(s.gpa <= 3),
               count(s.gpa > 3 and s.gpa <= 4),
               count(s.gpa > 4)) for g in Group for s in g.students)

# print(v1)
