from datetime import datetime
from zulu import Zulu
from zulu.parser import UTC, format_datetime

native = datetime(2020, 5, 24, 8, 20, 00, 137493, tzinfo=UTC)

format_datetime(native, '%Y-%m-%d %H:%M:%S%z')
# '2020-05-24 08:20:00+0000'

format_datetime(native, 'YYYY-MM-dd HH:mm:ssZ')
# '2020-05-24 08:20:00+0000'

dt = Zulu.fromdatetime(native)
format_datetime(dt, 'YYYY-MM-dd HH:mm:ssZ')
# '2020-05-24 08:20:00+0000'
