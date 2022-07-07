from delorean import Delorean
from datetime import datetime

d1 = Delorean(datetime(2021, 5, 24, 12, 15), timezone='Asia/Tokyo')
d2 = d1.replace(hour=8)

# print(d1)
# print(d2)
