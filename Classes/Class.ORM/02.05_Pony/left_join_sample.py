# from pony.orm.examples.estore import *
from estore import *
populate_database()

#v1 = select((c, count(o)) for c in Customer for o in c.orders)[:]

# print(v1)
