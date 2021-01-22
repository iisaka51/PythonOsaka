import orjson, datetime

# Python 3.9 stdlib
try:
    from zoneinfo import ZoneInfo as gettz
except:
    from dateutil.tz import gettz

data = orjson.dumps(
    datetime.datetime(2021, 12, 1, 2, 3, 4, 9,
                      tzinfo=gettz('Asia/Tokyo'))
)
print('  DATA:', repr(data))
print('NORMAL:', data)

data = orjson.dumps(
    datetime.datetime.fromtimestamp(4123518902)
    .replace(tzinfo=datetime.timezone.utc)
)
print('  DATA:', repr(data))
print('NORMAL:', data)

data = orjson.dumps(
    datetime.datetime.fromtimestamp(4123518902)
)
print('  DATA:', repr(data))
print('NORMAL:', data)
