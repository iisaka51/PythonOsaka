from estore import *

v1 = count(c for c in Customer if len(c.orders) > 1)

# print(v1)
