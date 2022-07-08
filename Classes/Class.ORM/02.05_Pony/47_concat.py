from estore import *

v1 = select(concat(p.name, ' ', p.country) for p in Customer)

# print(v1)
# print(v1.first())
