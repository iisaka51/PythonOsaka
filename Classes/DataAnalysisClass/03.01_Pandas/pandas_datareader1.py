from datetime import datetime
import pandas as pd
import pandas_datareader as pdr

start=datetime(2010, 1, 1)
end=datetime(2020, 1, 1)
df = pdr.DataReader("AAPL", 'yahoo', start, end)

print(df.head())
