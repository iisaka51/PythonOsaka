from mymodeldb import *
from pprint import pprint

v1 = MyModel.objects.all(_exclude='Sake')
v2 = list(v1)

v3 = MyModel.objects.all(_exclude=['Sake','Wine'])
v4 = list(v1)

# pprint(v1)
# pprint(v2)
# pprint(v3)
# pprint(v4)
