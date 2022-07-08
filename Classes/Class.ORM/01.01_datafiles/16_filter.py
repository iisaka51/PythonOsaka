from mymodeldb import *
from pprint import pprint

v1 = MyModel.objects.filter(my_value=3)
v2 = list(v1)

v3 = MyModel.objects.filter(my_value=3, _exclude='Sake')
v4 = list(v3)

# pprint(v1)
# pprint(v2)
# pprint(v3)
# pprint(v4)
