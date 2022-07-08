from datetime import *; from dateutil.relativedelta import *

NOW = datetime.now()
TODAY = date.today()
print(f'NOW: {NOW}')
print(f'TODAY: {TODAY}')

target_date = NOW+relativedelta(months=+1)
print(f'+1 month: {target_date}')

target_date = NOW+relativedelta(months=+1, weeks=+1)
print(f'+1 month and +1 week: {target_date}')

target_date = TODAY+relativedelta(months=+1, weeks=+1, hour=10)
print(f'+1 month and +1 week and +10 Hours: {target_date}')

target_date = NOW+relativedelta(year=1, month=1)
print(f'+1 Year and +1 month: {target_date}')

