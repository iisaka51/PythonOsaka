from dateutil.rrule import rrule, MONTHLY
from datetime import datetime

start_date = datetime(2020, 5, 24, 8, 20)
period = list(rrule(freq=MONTHLY, count=4, dtstart=start_date))

for dt in period:
    print(dt)
