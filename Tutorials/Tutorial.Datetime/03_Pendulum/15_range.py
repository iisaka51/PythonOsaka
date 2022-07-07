import pendulum

start = pendulum.datetime(2020, 5, 24)
end = pendulum.datetime(2020, 10, 2)
period = pendulum.period(start, end)

dt = pendulum.datetime(2020, 7, 22)
v1 = dt in period
assert v1 == True

for dt in period.range('months'):
    print(dt)
