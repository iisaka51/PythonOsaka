from datetime import *
import pytz

d1 = datetime(2020, 1, 1, 1, 2, 3, tzinfo=pytz.UTC)
d2 = datetime(2019, 12, 31, 22, 2, 3, tzinfo=pytz.UTC)
delta = d2 - d1

print(delta.days)
print(delta.seconds)
