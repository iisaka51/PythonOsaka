import pendulum

dt = pendulum.datetime(2020, 2, 2, 2, 2, 2, tz='Asia/Tokyo')
print(f'dt: {dt}')

cdt = dt.strftime('%A %-d%t of %B %Y %I:%M:%S %p')
print(f"dt.strftime('%A %-d%t of %B %Y %I:%M:%S %p'): \n     {cdt}")

cdt =  dt.format('dddd Do [of] MMMM YYYY HH:mm:ss A')
print(f"dt.format('dddd Do [of] MMMM YYYY HH:mm:ss A'): \n     {cdt}")

