from delorean import Delorean
from datetime import datetime, timedelta

d1 = Delorean()
d1s = f'{d1}'
d1 += timedelta(hours=2)
d2 = d1 - timedelta(hours=2)
d3 = d1 + timedelta(hours=2)
d4 = d2 - d1

# print(d1s)
# print(d1)
# print(d2)
# print(d3)
# print(d4)
