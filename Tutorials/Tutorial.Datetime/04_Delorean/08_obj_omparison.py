from delorean import Delorean
from datetime import datetime, timedelta

# JST = UTC+9
d1 = Delorean(datetime(2021, 9, 5, 9), timezone='Asia/Tokyo')
d2 = Delorean(datetime(2021, 9, 5), timezone='UTC')

v = d1 == d2

# print(d1)
# print(d2)
# print(v)
