from datetime import *
from dateutil.relativedelta import *

target_date = date(2020, 1, 1) + relativedelta(yearday=1)
print(f'90 days later from 2020/01/01 = {target_date}')

target_date = date(2020, 1, 1) + relativedelta(yearday=260)
print(f'90 days later from 2020/01/01 = {target_date}')

target_date = date(2019, 1, 1) + relativedelta(yearday=260)
print(f'90 days later from 2019/01/01 = {target_date}')

