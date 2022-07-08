import pandas as pd

df = pd.read_csv('titanic.csv')

v1 = df.groupby(['sex', 'survived'])['survived'].sum()
