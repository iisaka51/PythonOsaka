import arrow

start = arrow.get(2021, 12, 31, 22, 0)
end = arrow.get('2022-01-01 02:00')

for r in arrow.Arrow.range('hour', start, end):
  print(repr(r))

dt = arrow.get('2020-02-01 00:00')
dt.span('hour')
dt.span('month')

dt = arrow.get('2020-02-14 00:00')
dt.floor('month')
dt.ceil('month')
