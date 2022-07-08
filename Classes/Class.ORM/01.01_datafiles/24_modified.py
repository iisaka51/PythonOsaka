from mymodeldb import *

v1 = MyModel.objects.get('Beer')
s1 = f'{v1}'
!echo 'my_value: 6' > mymodels/Beer.yml

v2 = v1.datafile.modified
v3 = MyModel.objects.get('Beer')

v4 = v3.datafile.modified

# print(v1)
# print(s1)
# print(v2)
# print(v3)
# print(v4)
