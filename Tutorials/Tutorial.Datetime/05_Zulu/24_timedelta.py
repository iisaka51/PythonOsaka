import zulu

delta = zulu.parse_delta('1w 3d 2h 32m')
# <Delta [10 days, 2:32:00]>

assert isinstance(delta, zulu.Delta)

from datetime import timedelta
assert isinstance(delta, timedelta)

t1 = zulu.parse_delta('2:04:13:02.266')
# <Delta [2 days, 4:13:02.266000]>

t2 = zulu.parse_delta('2 days, 5 hours, 34 minutes, 56 seconds')
# <Delta [2 days, 5:34:56]>
