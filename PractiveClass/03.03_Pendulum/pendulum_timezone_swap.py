import pendulum

dt_tokyo = pendulum.datetime(2020, 2, 2, tz='Asia/Tokyo')

dt_newyork1 = dt_tokyo.in_timezone(tz='America/New_York')
dt_newyork2 = dt_tokyo.in_tz(tz='America/New_York')

print(dt_tokyo)
print(dt_newyork1)
print(dt_newyork2)
