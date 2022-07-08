from pipe import where

data = [1, 2, 3, 4, 5]
v1 = list(data | where(lambda x: x % 2 == 0))

# v1
