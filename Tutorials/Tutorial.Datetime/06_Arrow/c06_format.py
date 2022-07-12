import arrow

now = arrow.now()

year = now.format('YYYY')
print(f"Year: {year}")

date = now.format('YYYY-MM-DD')
print(f"Date: {date}")

date_time = now.format('YYYY-MM-DD HH:mm:ss')
print(f"Date and time: {date_time}")

date_time_zone = now.format('YYYY-MM-DD HH:mm:ss ZZ')
print(f"Date and time and zone: {date_time_zone}")
