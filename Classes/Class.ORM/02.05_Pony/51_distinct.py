from estore import *

v1 = distinct(o.date_shipped for o in Order)
v2 = select(sum(distinct(x.total_price)) for x in Order)

# print(v1)
# print(v2)
# print(v2.first())
