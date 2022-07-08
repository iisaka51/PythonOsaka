import pandas as pd

df = pd.read_csv('titanic.csv')

v1 = df['embark_town']
v2 = df['embark_town'].str.contains('town')
v3 = df['embark_town'].str.contains('^Q.*', regex=True)
