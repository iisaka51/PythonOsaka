import arrow

now = arrow.now()

d1 = now.shift(minutes=-15).humanize()
print(d1)

d1 = now.shift(minutes=-15).humanize(locale='ja')
print(d1)

d2 = now.shift(hours=5).humanize()
print(d2)

d2 = now.shift(hours=5).humanize(locale='ja')
print(d2)

