import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

start = dt.datetime(2015, 1, 1)
end = dt.datetime.now()
df = web.DataReader("TSLA", 'yahoo', start, end)
df.reset_index(inplace=True)
print(df.head())
df.set_index("Date", inplace=True)
# df = df.drop('',axis=1)
