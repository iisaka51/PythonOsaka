import arrow

start = arrow.get(2021, 12, 31, 22, 0)
end = arrow.get('2022-01-01 02:00')

for r in arrow.Arrow.range('hour', start, end):
  print(repr(r))
