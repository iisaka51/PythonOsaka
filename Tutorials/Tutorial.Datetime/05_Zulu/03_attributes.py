import zulu

dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')

assert dt.year == 2020
assert dt.month == 5
assert dt.day == 24
assert dt.hour == 8
assert dt.minute == 20
assert dt.second == 00
assert dt.microsecond == 137493
assert dt.tzname() == '+00:00'

# assert は与えた式が真のときは何も出力しない
