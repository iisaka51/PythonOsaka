data = frozenset([1, 2, 3])
print( 'remove' in dir(data))

data = set([1, 2, 3])
print( 'remove' in dir(data))

data.remove(3)
print(data)

data.remove(5)
print(data)
