import arrow

utc = arrow.utcnow()
print(utc)

epoch_time = utc.timestamp()
print(epoch_time)

date = arrow.Arrow.fromtimestamp(epoch_time)
print(date)
