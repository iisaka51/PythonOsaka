import pandas as pd

df = pd.read_csv('titanic.csv')

v1 = df.isnull().sum()
v2 = df.isnull().sum().sum()
v3 = df['age'].isnull().sum()
