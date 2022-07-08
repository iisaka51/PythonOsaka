data = frozenset([1, 2, 3])
print( 'discard' in dir(data))

data = set([1, 2, 3])
print( 'discard' in dir(data))

data.discard(3)
print(data)

data.discard(5)
print(data)
