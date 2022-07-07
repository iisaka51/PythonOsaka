from datetime import *
from dateutil.relativedelta import *

dt = date(2020,7,20)

date1 = dt + relativedelta(months=+1)
date2 = dt + relativedelta(months=+1, weeks=+1)
date3 = dt + relativedelta(months=+1, weeks=+1, hours=+10)
date4 = dt + relativedelta(years=+1, months=+1)


# Bad usage: can you say what's wrng?
date5 = dt + relativedelta(year=1, month=1)

# date1
# ...
# date5
