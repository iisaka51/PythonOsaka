import arrow

utc = arrow.utcnow()

jst = utc.to('Asia/Tokyo')
tokyo = utc.to('Asia/Tokyo').format('HH:mm:ss')
newyork = utc.to('America/New_York').format('HH:mm:ss')
london = (utc.to('Europe/London').format('HH:mm:ss'))

print(jst)
print(tokyo)
print(newyork)
print(london)
