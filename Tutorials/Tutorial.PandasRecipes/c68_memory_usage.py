import pandas as pd

df = pd.read_csv('TSLA.csv', parse_dates=["Date"])
v1 = df.memory_usage()
v2 = df.memory_usage().sum()
