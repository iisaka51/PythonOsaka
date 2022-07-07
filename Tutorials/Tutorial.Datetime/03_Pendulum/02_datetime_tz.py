import pendulum

dt_tokyo = pendulum.datetime(2020, 5, 24, tz='Asia/Tokyo')
dt_nyc = pendulum.datetime(2020, 5, 24, tz='America/New_York')
time_diff = dt_nyc.diff(dt_tokyo).in_hours()

# dt_tokyo
# dt_nyc
# time_diff
