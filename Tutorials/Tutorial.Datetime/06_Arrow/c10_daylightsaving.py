import arrow

now = arrow.now()

date_time = now.format("YYYY-MM-DD HH:mm:ss ZZ")
day_light_saving_Tokyo = now.dst()
day_light_saving_NY = now.to('America/New_York').dst()

print(date_time)
print(day_light_saving_Tokyo)
print(day_light_saving_NY)
