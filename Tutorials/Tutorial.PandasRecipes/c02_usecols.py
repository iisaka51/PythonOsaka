import pandas as pd

df = pd.read_csv("stockdata.csv", usecols=["Date", "stock", "value"])
