from mymodeldb import *

v1 = MyModel.objects.get('Beer')
before_dir = !ls mymodels
v2 = v1.datafile.path.unlink()
after_unlink = !ls mymodels
v3 = v1.datafile.save()
after_save = !ls mymodels

# print(before_dir)
# print(after_unlink)
# print(after_save)
