import pendulum

dt_tokyo = pendulum.datetime(2020, 3, 7, tz='Asia/Tokyo')
dt_newyork = pendulum.datetime(2020, 3, 7, tz='America/New_York')

print(dt_tokyo)
print(dt_newyork)
print(f'Time Difference: {dt_newyork.diff(dt_tokyo).in_hours()}')
