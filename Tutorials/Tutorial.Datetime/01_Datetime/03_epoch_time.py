from datetime import datetime, timezone, timedelta

utc_now = datetime.now(timezone.utc)
timezone_jst = timezone(timedelta(hours=9))

t1 = utc_now.timestamp()
t2 = utc_now.astimezone(timezone_jst)

# print(utc_now)
# print(t1)
# print(t2)
