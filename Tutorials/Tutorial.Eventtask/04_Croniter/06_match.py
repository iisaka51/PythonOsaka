from croniter import croniter
from datetime import datetime

v1 = croniter.match("0 0 * * *", datetime(2019, 1, 14, 0, 0, 0, 0))
v2 = croniter.match("0 0 * * *", datetime(2019, 1, 14, 0, 2, 0, 0))

dt = datetime(2019, 1, 1, 4, 2, 0, 0)
# 毎週水曜日 04:02 OR 毎月1日
v3 = croniter.match("2 4 1 * wed", dt)

# 毎週水曜日 04:02 AND 毎月1日
v4 = croniter.match("2 4 1 * wed", dt, day_or=False)

assert v1 == True
assert v2 == False
assert v3 == True
assert v4 == False
