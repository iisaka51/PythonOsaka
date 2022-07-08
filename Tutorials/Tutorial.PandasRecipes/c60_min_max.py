import pandas as pd

df = pd.read_csv('TSLA.csv', parse_dates=["Date"])

v1 = df['Adj Close'].idxmin()
v2 = df['Adj Close'].idxmax()

# df.iloc[v1]
# df.iloc[v2]
