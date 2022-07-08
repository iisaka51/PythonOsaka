import pandas as pd

df = pd.read_csv('TSLA.csv',
                 parse_dates=['Date'], index_col='Date')

df_w = df.resample('W').agg(
                  {'High': 'max', 'Low': 'min', 'Open': 'first',
                  'Close': 'last', 'Volume': 'sum', 'Adj Close': 'last' })
