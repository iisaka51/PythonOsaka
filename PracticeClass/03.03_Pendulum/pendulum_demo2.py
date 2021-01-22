from datetime import datetime
import pendulum

dt_now = datetime.now()
pt_now = pendulum.now()

print(f'datetime.now(): {dt_now}')
print(f'pendulum.now(): {pt_now}')

today = pendulum.today()
yesterday = pendulum.yesterday()
tomorrow = pendulum.tomorrow("America/New_York")

print(f'pendulum.today(): {today}')
print(f'pendulum.yesterday(): {yesterday}')
print(f'pendulum.tomorrow in NewYork(): {tomorrow}')
