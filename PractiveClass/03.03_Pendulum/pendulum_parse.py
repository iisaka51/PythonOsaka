import pendulum

dt = pendulum.parse('2020-02-02T02:02:02')
print(dt)

dt = pendulum.parse('2020-02-02T02:02:02', tz='America/New_York')
print(dt)

# NOT ISO-8601
dt = pendulum.parse('1975-05-21 22:00:00')

try:
    dt = pendulum.parse('31-01-01')
    print(dt)
except:
    print('pendulum parse error.')

dt = pendulum.parse('31-01-01', strict=False)
print(dt)
