from datetime import datetime
import zulu

dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')
# <Zulu [2020-05-24T08:20:00.137493+00:00]>

v1 = isinstance(dt, zulu.Zulu)
assert v1 == True

v2 = isinstance(dt, datetime)
assert v2 == True
