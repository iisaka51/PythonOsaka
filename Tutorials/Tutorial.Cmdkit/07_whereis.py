from cmdkit.config import Namespace

data = {'a': {'x': 1, 'y': 2},
        'b': {'x': 3, 'z': 4} }

ns = Namespace(data)

v1 = f'{ns}'
v2 = ns.whereis('x')
v3 = ns.whereis('x', 1)
v4 = ns.whereis('x', lambda v: v % 3 == 0)

# print(v1)
# ...
# print(v4)
