import pendulum

dt_tokyo = pendulum.datetime(2020, 5, 24, 8, 20, 0, tz="Asia/Tokyo")

dt1 = dt_tokyo.add(days=1)
dt2 = dt_tokyo.add(weeks=1)
dt3 = dt_tokyo.subtract(days=1)
dt4 = dt_tokyo.subtract(weeks=1)

# dt1
# ...
# dt4
