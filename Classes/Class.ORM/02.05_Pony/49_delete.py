from estore import *

v1 = delete(o for o in Order if o.state == CANCELLED)
v2 = delete(o for o in Order if o.state == DELIVERED)

# print(v1)
# print(v2)
