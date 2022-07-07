import pandas as pd

s = pd.Series([0,1,2,3,None,5,6,9,10,13,40])
df = pd.DataFrame(s)
df.isna()

from palmerpenguins import load_penguins
df = load_penguins()

null = df.isna().sum()/len(df)
null[null > 0].sort_values()
