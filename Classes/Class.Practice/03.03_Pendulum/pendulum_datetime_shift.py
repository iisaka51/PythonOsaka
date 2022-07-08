import pendulum

dt_tokyo = pendulum.datetime(2012, 2, 2, 1, 2, 3,
                             tz="Asia/Tokyo")
print(dt_tokyo)

help(dt_tokyo.subtract)
dt = dt_tokyo.add(days=1)
print(dt)
dt = dt_tokyo.add(weeks=1)
print(dt)
dt = dt_tokyo.subtract(days=1)
print(dt)
dt = dt_tokyo.subtract(weeks=1)
print(dt)
