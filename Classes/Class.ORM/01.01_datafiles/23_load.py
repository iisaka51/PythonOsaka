
!mv mymodels/Beer.yml .
before_load = !ls mymodels

from mymodeldb import *

v1 = MyModel('Beer', 20)
s1  = f'{v1}'

v2 = MyModel.objects.get('Beer')
s2  = f'{v2}'

!mv Beer.yml mymodels/Beer.yml
v3 = v2.datafile.load()

after_load = !ls mymodels
v4 = MyModel.objects.get('Beer')

# print(v1)
# print(s1)
# print(v2)
# print(s2)
# print(v3)
# print(v4)
