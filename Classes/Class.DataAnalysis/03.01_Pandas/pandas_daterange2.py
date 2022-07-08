import pandas as pd

dates = pd.date_range(start='2020/1/1', periods=5, freq='D')
timeseries = pd.Series(range(5), index=dates)

print(timeseries)

