from datetime import datetime
import pandas as pd
import pandas_datareader as pdr

start=datetime(1970, 1, 1)
end=datetime(2022, 5, 1)
stock_data = pdr.DataReader("^GSPC", 'yahoo', start, end)
stock_data.to_csv('SP500.csv')
