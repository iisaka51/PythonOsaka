import pendulum

dt = pendulum.datetime(2020, 2, 2, 2, 2, 2, tz='Asia/Tokyo')
print(f'dt: {dt}')

cdt = dt.isoformat()
print(f'dt.isoformat(): {cdt}')

cdt = dt.to_date_string()
print(f'dt.to_date_string(): {cdt}')

cdt = dt.to_formatted_date_string()
print(f'dt.to_formatted_date_string(): {cdt}')

cdt = dt.to_time_string()
print(f'dt.to_time_sting(): {cdt}')

cdt = dt.to_datetime_string()
print(f'dt.to_datetime_string(): {cdt}')

cdt = dt.to_day_datetime_string()
print(f'dt.to_day_datetime_string(): {cdt}')

cdt =  dt.format('dddd Do [of] MMMM YYYY HH:mm:ss A')
print(f"dt.format('dddd Do [of] MMMM YYYY HH:mm:ss A'): \n     {cdt}")

cdt = dt.strftime('%A %-d%t of %B %Y %I:%M:%S %p')
print(f"dt.strftime('%A %-d%t of %B %Y %I:%M:%S %p'): \n     {cdt}")
