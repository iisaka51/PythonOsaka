from croniter import croniter
from datetime import datetime
import dateutil.tz

tz = dateutil.tz.gettz('Asia/Tokyo')
local_date = datetime(2021, 3, 14, tzinfo=tz)
cron1 = croniter('* * * * * 1', local_date)

base = datetime(2012, 4, 6, 13, 26, 10)
cron2 = croniter('* * * * * 15,25', base)

print('1st...')
for i in range(3):
    print(cron1.get_next(datetime))

print('2nd...')
for i in range(3):
    print(cron2.get_next(datetime))

print('1st again...')
for i in range(3):
    print(cron1.get_next(datetime))

