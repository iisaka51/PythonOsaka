from cmdkit.config import Namespace

data = {'a': {'x': 1, 'y': 2}, 'b': 3}

ns = Namespace(data)

v1 = f'{ns}'
ns.update({'a': {'x': 4, 'z': 5}})

v2 = f'{ns}'

# print(v1)
# print(v2)
