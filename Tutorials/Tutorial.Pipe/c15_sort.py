from pipe import sort

data = [1, 2, 3, -4, 5]
v1 = list( data| sort())
v2 = list( data| sort(reverse=True))
v3 = list( data| sort(key=abs))

# v1
# v2
# v3
