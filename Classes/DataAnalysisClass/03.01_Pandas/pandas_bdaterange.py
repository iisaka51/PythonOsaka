import datetime
import pandas as pd

start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 3, 30)

weekmask = 'Mon Wed Fri'
holidays = [datetime.datetime(2020, 2, 11),
            datetime.datetime(2020, 2, 24),
            datetime.datetime(2020, 3, 22)]

dr_1 = pd.bdate_range(start, end, freq='C', weekmask=weekmask, holidays=holidays)
dr_2 = pd.bdate_range(start, end, freq='CBMS', weekmask=weekmask)

print(dr_1)
print(dr_2)
