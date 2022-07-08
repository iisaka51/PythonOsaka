import pandas as pd

df = pd.read_csv('stockdata.csv')

df = df.rename({"value": "price", "Date": "date"}, axis=1)
