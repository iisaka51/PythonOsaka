import pandas as pd

df = pd.read_csv('TSLA.csv',
                 parse_dates=['Date'], index_col='Date')

df_w = df.resample('W').agg(
                  {'High': 'max', 'Low': 'min', 'Open': 'first',
                  'Close': 'last', 'Volume': 'sum', 'Adj Close': 'last' })

df_w['EMA5'] = df_w["Close"].ewm(span=5, adjust=False).mean()
df_w['EMA25'] = df_w["Close"].ewm(span=25, adjust=False).mean()
df_w['EMA75'] = df_w["Close"].ewm(span=75, adjust=False).mean()
