import pandas as pd

df = pd.read_csv('titanic.csv')

v1 = df.isnull()
v2 = df['age'].isnull()
v3 = df['age'].isnull().values[:10]
v4 = df['age'].isnull().values.any()
