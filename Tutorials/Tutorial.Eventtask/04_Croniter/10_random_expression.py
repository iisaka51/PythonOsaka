from croniter import croniter
from datetime import datetime

cron = croniter("R R * * *")
print(cron.get_next(datetime))
print(cron.get_next(datetime))

cron = croniter("R R * * *")
print(cron.get_next(datetime))
