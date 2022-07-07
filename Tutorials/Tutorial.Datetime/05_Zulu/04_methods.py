import zulu

dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')

dt.utcoffset()
# datetime.timedelta(0)

dt.dst()
# datetime.timedelta(0)

dt.isoformat()
# '2020-05-24T08:20:00.137493+00:00'

dt.weekday()
# 6

dt.isoweekday()
# 7

dt.isocalendar()
# datetime.IsoCalendarDate(year=2020, week=21, weekday=7)

dt.ctime()
# 'Sun May 24 08:20:00 2020'

dt.toordinal()
# 737569

dt.timetuple()
# time.struct_time(tm_year=2020, tm_mon=5, tm_mday=24,
#                  tm_hour=8, tm_min=20, tm_sec=0,
#                  tm_wday=6, tm_yday=145, tm_isdst=-1)

dt.utctimetuple()
# time.struct_time(tm_year=2020, tm_mon=5, tm_mday=24,
#                  tm_hour=8, tm_min=20, tm_sec=0,
#                  tm_wday=6, tm_yday=145, tm_isdst=0)

dt.timestamp()
# 1590308400.137493

dt.date()
# datetime.date(2020, 5, 24)

dt.time()
# datetime.time(8, 20, 0, 137493)

dt.timetz()
# datetime.time(8, 20, 0, 137493,
#               tzinfo=datetime.timezone(datetime.timedelta(0), '+00:00'))
