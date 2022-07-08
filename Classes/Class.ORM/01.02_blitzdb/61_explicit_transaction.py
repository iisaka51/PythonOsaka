from model_sqldemo3 import *

# 明示的にトランザクションを開始
transaction = backend.begin()

beer = Beer({'name': 'Hysteric IPA', 'abv': 7.0, 'stock': 6})
backend.save(beer)
v1 = backend.current_transaction
v2 = backend._conn

backend.commit()
v3 = backend.current_transaction
v4 = backend._conn

# print(v1)
# ...
# print(v4)
