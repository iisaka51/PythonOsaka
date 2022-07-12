from datetime import datetime
import arrow

d1 = arrow.get('2020-05-24 08:20:30')
d2 = arrow.get('2020/05/24 08:20:30')
d3 = arrow.get(1590308430)
d4 = arrow.get(datetime(2022, 5, 24, 8, 20, 30))

print(d1)
print(d2)
print(d3)
print(d4)
