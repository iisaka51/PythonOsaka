import datetime as dt
import pandas as pd
import pandas_datareader.data as web

start = dt.datetime(2015, 1, 3)
end = dt.datetime.now()
df = web.DataReader("TSLA", 'yahoo', start, end)
df.reset_index(inplace=True)
print(df.head())
df.set_index("Date", inplace=True)
df.to_excel('test.xlsx')
