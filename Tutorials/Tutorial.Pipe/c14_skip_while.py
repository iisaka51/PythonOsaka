from pipe import skip_while

data = [1, 2, 3, 4, 5]
v1 = list( data| skip_while(lambda x: x < 3))

# v1
