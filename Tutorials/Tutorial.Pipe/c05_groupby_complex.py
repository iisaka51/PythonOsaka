from pipe import select, groupby, where

data = (1, 2, 3, 4, 5, 6, 7, 8, 9)
v1 = list( data
             | groupby(lambda x: "Even" if x % 2 == 0  else "Odd")
             | select(lambda x: { x[0]: list( x[1]
                                        | where(lambda x: x> 4))} ))

# v1
