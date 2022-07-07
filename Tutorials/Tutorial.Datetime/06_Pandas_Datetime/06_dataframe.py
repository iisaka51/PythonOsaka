import pandas as pd

df = pd.read_csv('GOOG.csv')
ts = df['Date']
tss = pd.to_datetime(ts)
t1 = f'{tss[2].year}年{tss[2].month}月{tss[2].day}日'

# print(df.head())
# print(ts.head())
# print(tss.head())
# print(t1)
