import numpy as np
import pandas as pd

df = pd.read_csv('stockdata.csv', parse_dates=["Date"])

df1 = df[(df["Date"] > "2012-01-01") & (df["Date"] < "2013-06-01")]
