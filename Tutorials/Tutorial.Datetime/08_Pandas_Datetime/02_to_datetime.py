import pandas as pd

t1 = pd.to_datetime('2021-09-05')
t2 = pd.to_datetime('2021/09/05')
t3 = pd.to_datetime('2021,09,05')
t4 = pd.to_datetime('2021-09-05', format='%Y-%d-%m')

# print(t1)
# ...
# print(t4)
