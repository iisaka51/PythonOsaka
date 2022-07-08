import pandas as pd

df = pd.read_csv('stockdata.csv')

df = df.add_prefix('PRE_')
df = df.add_suffix('_SUF')
