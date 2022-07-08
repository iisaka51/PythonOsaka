from pipe import dedup

data = [1, 2, 2, 3, 3, 3, 4, 4, 5, 6, 7, 7, 7, 8,  9]
v1 = list(data | dedup( lambda key: key < 5))

# v1
