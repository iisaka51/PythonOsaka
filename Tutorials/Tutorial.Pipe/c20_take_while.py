from pipe import take_while

data = [1, 2, 3, 4, 5]
v1 = list( data| take_while(lambda x: x<3))

# v1
