import arrow

d1 = arrow.get('1962-01-13')

weekday_no = d1.weekday()
weekday = d1.format('dddd')

print(weekday_no)
print(weekday)
