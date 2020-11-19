data = frozenset([1, 2, 3])
print( 'add' in dir(data))

data = set([1, 2, 3])
print( 'add' in dir(data))

data.add(5)
print(data)

data.add(5)
print(data)
