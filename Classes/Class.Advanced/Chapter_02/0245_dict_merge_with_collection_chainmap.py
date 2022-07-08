from collections import ChainMap

x = {'a':1, 'b':2}
y = {'c':3, 'd':4}

z = dict(ChainMap(x, y))
print(z)
