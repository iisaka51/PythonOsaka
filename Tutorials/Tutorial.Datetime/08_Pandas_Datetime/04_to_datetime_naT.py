import pandas as pd
import numpy as np

d1 = pd.Series(['2021-09-01', np.nan, '2021-09-03', '2021-09-04'])
t1 = pd.to_datetime(d1, format='%Y-%m-%d')

# print(t1)
