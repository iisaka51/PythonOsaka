from datetime import *
from dateutil.relativedelta import *

dt = date(2020,7,20)

date1 = dt + relativedelta(month=1, day=1)
v1 = date1.weekday()
v2 = date1.strftime('%A')

date2 = dt + relativedelta(month=2, day=31)
v3 = date2.weekday()
v4 = date2.strftime('%A')

# date1
# v1
# v2
# date2
# v3
# v4
