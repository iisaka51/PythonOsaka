import zulu

t1 = zulu.to_seconds(seconds=5, minutes=2, hours=3, days=2, weeks=1)
assert t1 == 788525.0

t2 = zulu.to_seconds(milliseconds=25300, seconds=5, minutes=2)
assert t2 == 150.3
