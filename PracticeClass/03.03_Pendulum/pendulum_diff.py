import pendulum

d1 = pendulum.datetime(2012, 1, 1, 1, 2, 3)
d2 = pendulum.datetime(2011, 12, 31, 22, 2, 3)
delta = d2 - d1

print(delta.days)
print(delta.hours)
