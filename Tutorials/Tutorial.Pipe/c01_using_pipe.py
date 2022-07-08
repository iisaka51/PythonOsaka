from pipe import where, select

data = [1, 2, 3, 4, 5]

# map() と filter() を同時に使用するとわかりにくい
v1 = list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0, data)))

# pipe を使うとコードがわかりやすくなる
v2 = list( data
           | where(lambda x: x % 2 == 0)
           | select(lambda x: x * 2) )
