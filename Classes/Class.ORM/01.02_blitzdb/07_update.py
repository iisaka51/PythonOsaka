from model_beerdb import *

v1 = backend.get(Beer, {'name': 'Pale Ale'})
v2 = v1.stock
v1.stock -= 2
backend.commit()

# print(v1)
# print(v2)
# print(v1.stock)
