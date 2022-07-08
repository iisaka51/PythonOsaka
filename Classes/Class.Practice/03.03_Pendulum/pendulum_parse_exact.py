import pendulum

dt = pendulum.parse('2012-05-03')
print(dt)
dt = pendulum.parse('2012-05-03', exact=True)
print(dt)

dt = pendulum.parse('12:04:23')
print(dt)
dt = pendulum.parse('12:04:23', exact=True)
print(dt)
