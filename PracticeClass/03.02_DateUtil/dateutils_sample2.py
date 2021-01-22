from datetime import *; from dateutil.relativedelta import *
import calendar

NOW = datetime.now()
TODAY = date.today()

# target_date = TODAY + relativedelta(weekday=calendar.SATURDAY)
# print(target_date)

epoch = date(1970,1,1)
print(TODAY)
print(relativedelta(epoch, TODAY))
