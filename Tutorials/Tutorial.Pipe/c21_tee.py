from pipe import tee

data = [1, 2, 3, 4, 5]
v1 = sum( data | tee )

# v1
