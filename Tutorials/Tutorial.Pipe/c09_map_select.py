from pipe import select, map

data = [1, 2, 3, 4, 5]
v1 = list( data | select(lambda x: x * 2) )
v2 = list( data | map(lambda x: x * 2) )

# v1
# v2
