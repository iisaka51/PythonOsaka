import fnc

data = [[1, 2], [3, [4, 5]]]

v1 = fnc.sequences.flatten(data)
v2 = fnc.sequences.flattendeep(data)

# list(v1)
# list(v2)
