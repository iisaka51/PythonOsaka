import pendulum

dt = pendulum.datetime(2020, 3, 4, tz='UTC')
# assert は与えた式が真のときは何も表示しない

dt1 = pendulum.parse('2020/03/04')
assert dt == dt1

dt2 = pendulum.parse('2020-03-04')
assert dt == dt2

# dateutil ではOKだけで、pendulum ではエラーになるパターン
# dt3 = pendulum.parse('2020/Mar/04')
# dt4 = pendulum.parse('2020-March-04')
# dt5 = pendulum.parse('04-Mar-2020')
# dt6 = pendulum.parse('04-March-2020')
# dt7 = pendulum.parse('04-Mar-20')
# dt8 = pendulum.parse('04-March-20')

dt2 = pendulum.datetime(2020, 3, 4, 2, 2, 2, tz='UTC')
dt10 = pendulum.parse('2020-03-04T02:02:02')
assert dt2 == dt10

dt3 = pendulum.datetime(2020, 3, 4, 2, 2, 2, tz='America/New_York')
dt11 = pendulum.parse('2020-03-04T02:02:02', tz='America/New_York')
assert dt3 == dt11

# NOT ISO-8601
dt12 = pendulum.parse('2020-03-04 02:02:02')
assert dt2 == dt12

try:
    dt13 = pendulum.parse('31-01-01')
except:
    dt13 = 'pendulum parse error'

assert dt13 == 'pendulum parse error'

dt4 = pendulum.datetime(2031, 1, 1)
dt14 = pendulum.parse('31-01-01', strict=False)
assert dt4 == dt14
