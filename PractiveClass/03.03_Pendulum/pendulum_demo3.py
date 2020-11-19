from datetime import *
import pendulum

pt = pendulum.from_format('2020-02-02 02:02:02', 'YYYY-MM-DD hh:mm:ss')
pt_NY = pendulum.from_format('2020-02-02 02:02:02', 'YYYY-MM-DD hh:mm:ss',
                             tz='America/New_York')
print(type(pt))
print(pt)
print(pt_NY)

dt = datetime(2020, 2, 2)
pt = pendulum.instance(dt)
print(dt)
print(pt)

