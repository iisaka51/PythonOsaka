from datetime import datetime, timedelta
import pandas as pd
import pandas_datareader as pdr
from requests_cache import CachedSession

expire_after = timedelta(days=3)
session = CachedSession(cache_name='cache',
                        backend='sqlite', expire_after=expire_after)

start=datetime(2010, 1, 1)
end=datetime(2020, 1, 1)
df = pdr.DataReader("AAPL", 'yahoo', start, end, session=session)

print(df.head())
