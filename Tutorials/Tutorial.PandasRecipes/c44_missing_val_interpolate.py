import pandas as pd

df = pd.read_csv('titanic.csv')

v1 = df['age']
v2 = df['age'].interpolate(method='linear')
v3 = df['age'].interpolate(option='spline')
