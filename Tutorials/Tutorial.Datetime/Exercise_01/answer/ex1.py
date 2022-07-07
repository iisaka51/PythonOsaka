from flight_data import flight_data
from dateutil.relativedelta import *
from dateutil.parser import parse
from dateutil.tz import gettz

departure = [parse(x, dayfirst=False,
                      tzinfos=gettz(flight_data['departure_tz'][i]))
             for i, x in enumerate(flight_data['departure']) ]
