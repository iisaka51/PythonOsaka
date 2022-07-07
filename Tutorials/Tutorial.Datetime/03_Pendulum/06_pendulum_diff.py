import pendulum

d1 = pendulum.datetime(2020, 1, 1, 1, 2, 3)
d2 = pendulum.datetime(2019, 12, 31, 22, 2, 3)

delta = d2 - d1
v1 = delta.days
v2 = delta.seconds
v3 = delta.hours

attrs = [attr for attr in dir(delta) if not attr.startswith('_')]

# v1
# v2
# v3
# attrs
