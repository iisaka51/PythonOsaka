import pandas as pd

df = pd.read_csv('titanic.csv')

v1 = df.columns
v2 = df.columns.str.upper()
v3 = df.columns.str.replace('survived', 'SURVIVED')

df.columns = v2
