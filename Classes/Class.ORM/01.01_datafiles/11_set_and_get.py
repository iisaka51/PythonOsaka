from mymodeldb import *

v1 = MyModel('Beer', 2)
v2 = MyModel.objects.get('Beer')

# print(v1)
# print(v2)
# !cat mymodels/Beer.yml
