from mymodeldb import *
from pprint import pprint

v1 = MyModel.objects.all()
v2 = list(v1)

v3 = MyModel.objects.all(_exclude='Sake')
v4 = list(v3)

# pprint(v1)
# pprint(v2)
# pprint(v3)
# pprint(v4)
