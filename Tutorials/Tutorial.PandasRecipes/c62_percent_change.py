import pandas as pd

df = pd.read_csv('TSLA.csv', parse_dates=["Date"])
df['Change'] = df['Adj Close'].pct_change()
