import pandas as pd

s1 = pd.Series(range(5))
s2 = pd.Series([1, 2, 3], index=['One', 'Two', 'Three'])
s3 = pd.Series({'One':1, 'Two':2, 'Three':3})

print(s3)
s3 = s3.append(pd.Series({'Four':4}))
print(s3)
