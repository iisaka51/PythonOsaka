import orjson, datetime

data = orjson.dumps(
        datetime.datetime(2021, 1, 1, 0, 0, 0, 1),
    )
print(data)

data = orjson.dumps(
        datetime.datetime(2021, 1, 1, 0, 0, 0, 1),
        option=orjson.OPT_OMIT_MICROSECONDS,
    )
print(data)
