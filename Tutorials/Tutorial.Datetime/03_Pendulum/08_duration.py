import pendulum

it = pendulum.duration(years=2, months=3,
                       days=1177, seconds=7284, microseconds=1234)

dt01 = it.years
dt02 = it.months
dt03 = it.weeks
dt04 = it.days
dt05 = it.hours
dt06 = it.seconds
dt07 = it.total_weeks()
dt08 = it.total_days()
dt09 = it.total_hours()
dt10 = it.total_minutes()
dt11 = it.total_seconds()
dt12 = it.in_weeks()
dt13 = it.in_days()
dt14 = it.in_hours()
dt15 = it.in_minutes()
dt16 = it.in_seconds()

assert dt01 == 2
assert dt02 == 3
assert dt03 == 168
assert dt04 == 1997
assert dt05 == 2
assert dt06 == 7284
assert dt07 == 285.2977579385483
assert dt08 == 1997.0843055698379
assert dt09 == 47930.02333367611
assert dt10 == 2875801.400020567
assert dt11 == 172548084.001234
assert dt12 == 285
assert dt13 == 1997
assert dt14 == 47930
assert dt15 == 2875801
assert dt16 == 172548084

attrs = [attr for attr in dir(it) if not attr.startswith('_')]
# attrs
