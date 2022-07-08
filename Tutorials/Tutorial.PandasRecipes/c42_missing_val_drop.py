import pandas as pd

df = pd.read_csv('titanic.csv')

v1 = df.isnull().sum()

df1 = df.dropna(axis=0)
v2 = df1.isnull().sum()

df2 = df.dropna(axis=1)
v3 = df2.isnull().sum()
