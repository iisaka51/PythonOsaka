from croniter import croniter_range
from datetime import datetime

start_dt = datetime(2019, 1, 1)
stop_dt = datetime(2019, 12, 31)
step = "0 0 * * sat#1"

for dt in croniter_range(start_dt, stop_dt, step):
    print(dt)
