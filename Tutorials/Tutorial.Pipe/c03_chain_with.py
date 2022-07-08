from pipe import chain, chain_with

data1 = [[1, 2, [3]], [4, 5]]
data2 = [6, 7]
v1 = list( data1 | chain_with(data2) )

# v1
