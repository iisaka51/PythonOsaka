import arrow

utc = arrow.utcnow()

epoch_time = utc.format('X')

print(utc)
print(epoch_time)
