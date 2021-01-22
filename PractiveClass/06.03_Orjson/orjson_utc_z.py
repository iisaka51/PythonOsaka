import orjson, datetime

date_obj = datetime.datetime(2021, 1, 1, 0, 0, 0,
                             tzinfo=datetime.timezone.utc)
data = orjson.dumps(date_obj)
print('  DATA:', data)
print('NORMAL:', data)

data = orjson.dumps(
        date_obj,
        option=orjson.OPT_UTC_Z
    )
print(' UTC_Z:', data)
