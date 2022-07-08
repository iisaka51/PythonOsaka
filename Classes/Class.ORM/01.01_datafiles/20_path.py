from mymodeldb import *

v1 = MyModel.objects.get('Beer')
v2 = v1.datafile.path

# print(v1)
# print(v2)
# print(v2.parts[-1])
# print(v2.parent)
