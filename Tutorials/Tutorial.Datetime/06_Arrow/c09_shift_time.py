import arrow

now = arrow.now()
later_5h = now.shift(hours=5).time()
later_5d = now.shift(days=5).date()
before_3y = now.shift(years=-3).date()

print(later_5h)
print(later_5d)
print(before_3y)
