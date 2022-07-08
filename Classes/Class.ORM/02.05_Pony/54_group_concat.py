from estore import *

v1 = group_concat((c.name for c in Customer), sep=',')

# print(v1)
