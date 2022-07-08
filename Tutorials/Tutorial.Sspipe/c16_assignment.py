import pandas as pd

df = pd.read_csv('data.csv')

df1 = df.copy()
X = df1['Name']
X = X.str.upper()
df1['Name'] = X


from sspipe import p, px
df2 = df.copy()
df2['Name'] |= px.str.upper()
