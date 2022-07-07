import zulu
dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')

dt.naive
# datetime.datetime(2020, 5, 24, 8, 20, 0, 137493)

dt.datetime
# datetime.datetime(2020, 5, 24, 8, 20, 0, 137493,
#          tzinfo=datetime.timezone(datetime.timedelta(0), '+00:00'))

dt.is_leap_year()
# True

dt.days_in_month()
# 31

dt.datetuple()
# Date(year=2020, month=5, day=24)

dt.datetimetuple()
# DateTime(year=2020, month=5, day=24,
#          hour=8, second=20, minute=0, microsecond=137493,
#          tzinfo=datetime.timezone(datetime.timedelta(0), '+00:00'))
