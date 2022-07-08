from datetime import *
from dateutil.relativedelta import *
import calendar

NOW = datetime.now()
TODAY = date.today()

target_date = TODAY + relativedelta(weekday=FR)
print(f'Next Friday: {target_date}')
target_date = TODAY + relativedelta(weekday=FR(2))
print(f'Next, Next Friday: {target_date}')
target_date = TODAY + relativedelta(weekday=FR(-1))
print(f'Previous Friday: {target_date}')

target_date = TODAY + relativedelta(weekday=calendar.FRIDAY)
print(f'Next Friday: {target_date}')

target_date = TODAY + relativedelta(day=31, weekday=FR(-1))
print(f'This month latest Friday: {target_date}')
target_date = TODAY + relativedelta(months=-1, day=31, weekday=FR(-1))
print(f'Last Friday of previous month: {target_date}')
