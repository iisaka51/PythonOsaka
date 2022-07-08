from croniter import croniter
from datetime import datetime

base = datetime(2021, 10, 2, 12, 00)
cron = croniter('*/2 * * * *', base)  # 2分ごとに実行

print('get_next()...')
print(cron.get_next(datetime))
print(cron.get_next(datetime))
print(cron.get_next(datetime))

print('get_prev()...')
print(cron.get_prev(datetime))
print(cron.get_prev(datetime))
print(cron.get_prev(datetime))
