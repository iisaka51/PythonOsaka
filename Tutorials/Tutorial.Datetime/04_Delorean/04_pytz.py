import pytz
from pprint import pprint

v1 = pytz.common_timezones
v2 = [zone for zone in pytz.common_timezones if 'Tokyo' in zone]

# pprint(v1)
# print(v2)
