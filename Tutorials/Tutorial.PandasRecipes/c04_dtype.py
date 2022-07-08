import pandas as pd

df1 = pd.read_csv('stockdata.csv')
df2 = pd.read_csv('stockdata.csv', dtype={"stock": "category"})
