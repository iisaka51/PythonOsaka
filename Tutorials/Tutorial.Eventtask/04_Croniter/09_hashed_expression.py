from croniter import croniter
from datetime import datetime

cron = croniter("H H * * *", hash_id="hello")
print(cron.get_next(datetime))
print(cron.get_next(datetime))

cron = croniter("H H * * *", hash_id="hello")
print(cron.get_next(datetime))

cron = croniter("H H * * *", hash_id="bonjour")
print(cron.get_next(datetime))
