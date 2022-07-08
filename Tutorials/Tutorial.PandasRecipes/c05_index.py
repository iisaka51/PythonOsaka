import pandas as pd

df = pd.read_csv('stockdata.csv',
                 index_col="Date", parse_dates=["Date"])
