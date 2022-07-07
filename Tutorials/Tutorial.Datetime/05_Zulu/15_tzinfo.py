from datetime import datetime
import zulu

dt = zulu.parse('2020-05-24T08:20:00.137493+09:00')
local = dt.astimezone()
# same as doing dt.astimezone('local')
# datetime.datetime(2016, 7, 25, 15, 33, 18, 137493,
#                   tzinfo=tzlocal())

jst1 = dt.astimezone('Asia/Tokyo')

import pytz
jst2 = dt.astimezone(pytz.timezone('Asia/Tokyo'))

# jst1
# OUT: datetime.datetime(2020, 5, 24, 8, 20, 0, 137493,
#                        tzinfo=tzfile('/usr/share/zoneinfo/Asia/Tokyo'))

# jst2
# OUT: datetime.datetime(2020, 5, 24, 8, 20, 0, 137493,
#                        tzinfo=<DstTzInfo 'Asia/Tokyo' JST+9:00:00 STD>)
