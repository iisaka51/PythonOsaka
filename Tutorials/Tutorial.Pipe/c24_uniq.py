from pipe import uniq

data = [1, 1, 2, 2, 3, 3, 2, 1, 2, 3]
v1 = list(data | uniq)
v2 = list(data | uniq(key=lambda x: x % 2))

# v1
# v2
