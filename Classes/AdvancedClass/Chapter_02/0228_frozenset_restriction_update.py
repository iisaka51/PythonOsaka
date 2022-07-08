data = frozenset([1, 2, 3])
print( 'update' in dir(data))

data = set([1, 2, 3])
print( 'update' in dir(data))

data.update([2, 4])
print(data)

data.update((3, 6))
print(data)

data.update('Python')
print(data)

data.update(1)
print(data)
