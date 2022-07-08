from croniter import croniter
from datetime import datetime
import dateutil.tz

tz = dateutil.tz.gettz('Asia/Tokyo')
local_date = datetime(2021, 3, 14, tzinfo=tz)
cron = croniter('0 */1 * * *', local_date)

for i in range(5):
    print(cron.get_next(datetime))
