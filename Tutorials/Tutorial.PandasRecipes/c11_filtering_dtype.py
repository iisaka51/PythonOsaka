import pandas as pd

df = pd.read_csv('stockdata.csv',
                 dtype={"stock": "category"},
                 index_col="Date", parse_dates=["Date"])

df1 = df.select_dtypes(include="float64")
df2 = df.select_dtypes(include=["category", "int64"])
df3 = df.select_dtypes(exclude="int64")
