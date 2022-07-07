from datetime import *
from dateutil.relativedelta import *
import calendar

dt = date(2020,5,24)

# 次の金曜日
date1 = dt + relativedelta(weekday=FR)

# 次の次の金曜日
date2 = dt + relativedelta(weekday=FR(2))

# 前の金曜日
date3 = dt + relativedelta(weekday=FR(-1))

# 次の金曜日
date4 = dt + relativedelta(weekday=calendar.FRIDAY)

# 今月の前の金曜日
date5 = dt + relativedelta(day=31, weekday=FR(-1))

# 先月の直近の金曜日
date6 = dt + relativedelta(months=-1, day=31, weekday=FR(-1))

# date1
# ...
# date6
# !cal -3 5 2020
