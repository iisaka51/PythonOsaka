import arrow

utc = arrow.utcnow()
local = utc.to('local')

print(utc)
print(local)
