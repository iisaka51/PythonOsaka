from delorean import Delorean
from datetime import datetime

d1 = Delorean(datetime=datetime(2021, 5, 24, 8, 30, 00, 555555),
              timezone="Asia/Tokyo")
d2 = d1.truncate('month')
d3 = d1.truncate('year')

# print(d1)
# print(d2)
# print(d3)
