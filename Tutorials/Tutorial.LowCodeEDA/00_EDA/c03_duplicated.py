import pandas as pd

s = pd.Series([1,1,2,3,4,5,6,9,10,13,40])
df = pd.DataFrame(s)

df.duplicated().sum()
