from mymodeldb import *

v1 = MyModel.objects.get('Beer')
s1 = f'{v1}'
v2 = v1.datafile.data

# print(v1)
# print(s1)
# print(v2)
