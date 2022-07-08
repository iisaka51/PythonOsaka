from model_sqldemo import *

v1 = backend.get(Beer, {'name': 'Pale Ale'})
v2 = backend.get(Beer, dict(name='Pale Ale'))

# print(v1)
# print(v1.name)
# print(v1.abv)
# print(v2)
# print(v2.name)
# print(v2.abv)
