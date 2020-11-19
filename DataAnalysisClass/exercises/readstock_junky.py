from datetime import datetime
from pandas_datareader import data as pdr
import pandas as pd

start=datetime(2015,1,1)
end=datetime.now()
df = pdr.get_data_yahoo('MSFT', start, end)
df.to_csv('MSFT.csv')
