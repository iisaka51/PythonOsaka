import pandas as pd

df = pd.read_csv('titanic.csv')

v1 = df['age']
v2 = df['age'].fillna(0)
v3 = df['age'].fillna(method='ffill')
v4 = df['age'].fillna(method='bfill')

v_avg = df['age'].fillna(v1.mean())
v_median = df['age'].fillna(v1.median())
v_mode = df['age'].fillna(v1.mode().to_list()[0])
