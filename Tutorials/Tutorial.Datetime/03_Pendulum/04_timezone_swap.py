import pendulum

dt_tokyo = pendulum.datetime(2020, 2, 2, tz='Asia/Tokyo')

dt_nyc1 = dt_tokyo.in_timezone(tz='America/New_York')
dt_nyc2 = dt_tokyo.in_tz(tz='America/New_York')

# dt_tokyo
# dt_nyc1
# dt_nyc2
