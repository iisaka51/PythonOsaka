from datetime import *
from dateutil.relativedelta import *

TODAY = date.today()
print(f'TODAY: {TODAY}')

target_date = TODAY + relativedelta(month=1, day=1)
print(target_date)
print(target_date.weekday())
print(target_date.strftime('%A'))

target_date = TODAY + relativedelta(month=2, day=31)
print(target_date)
print(target_date.weekday())
print(target_date.strftime('%A'))
