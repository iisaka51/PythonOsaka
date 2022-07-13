import pandas as pd

d1 = pd.Series(['2021-09-01', '2021-09-02', '2021-09-03', '2021-09-04'])
t1 = pd.to_datetime(d1, format='%Y-%m-%d')
v1 = f'{t1[3].month}月{t1[3].day}日'

# print(t1)
# print(v1)
