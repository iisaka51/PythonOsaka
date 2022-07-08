from model_sqldemo3 import *

beer = Beer({'name': 'Hysteric IPA', 'abv': 7.0, 'stock': 6})

# 自動的にコミットされる
backend.save(beer)
v1 = backend.current_transaction
v2 = backend._conn
v3 = backend.get(Beer, {'name': 'Hysteric IPA'})

# print(v1)
# print(v2)
# print(v3)
