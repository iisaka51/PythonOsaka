from mymodeldb import *

v1 = MyModel.objects.get_or_none('Sake')
v2 = MyModel.objects.get_or_create('Sake', 3)
v3 = MyModel.objects.get_or_create('Sake')

# print(v1)
# print(v2)
# print(v3)
# !ls mymodels
# !cat mymodels/Sake.yml
