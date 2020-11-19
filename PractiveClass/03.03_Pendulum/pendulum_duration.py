import pendulum

it = pendulum.duration( days=80)
print(it)

t = it.years
print(f'it.years: {t}')
t = it.months
print(f'it.months: {t}')
t = it.weeks
print(f'it.weeks: {t}')
t = it.days
print(f'it.days: {t}')
t = it.hours
print(f'it.hours: {t}')
t = it.seconds
print(f'it.seconds: {t}')

t = it.total_weeks()
print(f'it.total_weeks(): {t}')
t = it.in_weeks()
print(f'it.in_weeks(): {t}')

t = it.total_days()
print(f'it.total_days(): {t}')
t = it.in_days()
print(f'it.in_days(): {t}')

t = it.total_hours()
print(f'it.total_hours(): {t}')
t = it.in_hours()
print(f'it.in_hours(): {t}')
