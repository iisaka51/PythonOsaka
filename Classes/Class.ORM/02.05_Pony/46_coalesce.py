from estore import *

v1 = select(coalesce(p.description, '') for p in Product)

# print(v1)
# print(v1.first())
