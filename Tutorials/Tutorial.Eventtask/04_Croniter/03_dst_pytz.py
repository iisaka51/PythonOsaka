import pytz
from croniter import croniter
from datetime import datetime

tz = pytz.timezone("America/New_York")
local_date = tz.localize(datetime(2021, 3, 24, 0, 0))

cron = croniter('0 */1 * * *', local_date)

print('get_next()...')
for i in range(5):
    print(cron.get_next(datetime))
