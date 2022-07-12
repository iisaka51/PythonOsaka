import arrow

local = arrow.now()
utc = local.to('UTC')

print(local)
print(utc)
