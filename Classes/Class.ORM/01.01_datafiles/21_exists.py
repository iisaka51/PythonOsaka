from mymodeldb import *

v1 = MyModel.objects.get('Beer')
v2 = v1.datafile.exists

# print(v1)
# print(v2)
