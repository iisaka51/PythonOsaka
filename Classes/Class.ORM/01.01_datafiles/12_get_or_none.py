from mymodeldb import *

v1 = MyModel.objects.get_or_none('Wine')
v2 = MyModel('Wine', 3)
v3 = MyModel.objects.get_or_none('Wine')

# print(v1)
# print(v2)
# print(v3)
