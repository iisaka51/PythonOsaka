from pipe import islice

data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
v1 = list( data | islice(2, 8, 2))

# v1
