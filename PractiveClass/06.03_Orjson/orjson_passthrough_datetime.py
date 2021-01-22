import orjson, datetime

def custom_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%a, %d %b %Y %H:%M:%S GMT")
    raise TypeError

date_dict = {"created_at": datetime.datetime(2021, 1, 1)}

data = orjson.dumps(date_dict)
print('  DATA:', repr(data))
print('NORMAL:', data)

try:
    data = orjson.dumps(
                date_dict,
                option=orjson.OPT_PASSTHROUGH_DATETIME
            )
except TypeError as msg:
    print('ERROR:', msg)

data = orjson.dumps(
            date_dict,
            option=orjson.OPT_PASSTHROUGH_DATETIME,
            default=custom_datetime,
    )
print('CUSTOM:', data)
