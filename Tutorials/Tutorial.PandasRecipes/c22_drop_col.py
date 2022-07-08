import pandas as pd

df = pd.read_csv('titanic.csv')

df1 = df.drop(['Unnamed: 0', 'who', 'embark_town'], axis=1)
