from datetime import *
import pytz

d1 = datetime(2020, 1, 1, 1, 2, 3, tzinfo=pytz.UTC)
d2 = datetime(2019, 12, 31, 22, 2, 3, tzinfo=pytz.UTC)
delta = d2 - d1

v1 = delta.days
v2 = delta.seconds
attrs = [attr for attr in dir(delta) if not attr.startswith('_')]

# v1
# v2
# attrs
