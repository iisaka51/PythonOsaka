import pandas as pd

df = pd.read_csv('stockdata.csv', parse_dates=["Date"])

df1 = df[df["Date"].dt.strftime("%Y-%m-%d") == "2007-01-03"]
df2 = df[df["Date"].dt.strftime("%m") == "12"]
df3 = df[df["Date"].dt.strftime("%Y") == "2012"]
