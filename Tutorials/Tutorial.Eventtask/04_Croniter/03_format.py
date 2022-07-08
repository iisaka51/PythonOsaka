from croniter import croniter
from datetime import datetime
import sys

base = datetime(2021, 10, 2, 12, 00)

print('# 月、金の 04:02')
cron = croniter('2 4 * * mon,fri', base)
print(cron.get_next(datetime))
print(cron.get_next(datetime))
print(cron.get_next(datetime))

print('# 毎週水曜日と毎月１日の04:02')
cron = croniter('2 4 1 * wed', base)
print(cron.get_next(datetime))
print(cron.get_next(datetime))
print(cron.get_next(datetime))


print('# 毎月1日の水曜日のときの 04:02')
cron = croniter('2 4 1 * wed', base, day_or=False)
print(cron.get_next(datetime))
print(cron.get_next(datetime))
print(cron.get_next(datetime))

print('# 毎月の第1土曜日と第2日曜日')
cron = croniter('0 0 * * sat#1,sun#2', base)
print(cron.get_next(datetime))
print(cron.get_next(datetime))
print(cron.get_next(datetime))
