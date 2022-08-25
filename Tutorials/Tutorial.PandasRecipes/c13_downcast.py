import pandas as pd

df = pd.read_csv('stockdata.csv')

df1 = df.copy()
df1['Unnamed: 0'] = pd.to_numeric(df1['Unnamed: 0'], downcast="integer")
df1['value'] = pd.to_numeric(df1['value'], downcast="float")
df1['change'] = pd.to_numeric(df1['change'], downcast="float")
