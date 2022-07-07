from delorean import Delorean
from pytz import timezone
from datetime import datetime

tz = timezone("Asia/Tokyo")
dt = tz.localize(datetime.utcnow())
d1 = Delorean(datetime=dt)

d2 = Delorean(datetime=dt, timezone="Asia/Tokyo")

# print(dt)
# print(d1)
# print(d2)
