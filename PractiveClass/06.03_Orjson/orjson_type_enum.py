import enum, datetime, orjson

class DatetimeEnum(enum.Enum):
    EPOCH = datetime.datetime(2021, 1, 1, 0, 0, 0)

data = orjson.dumps(DatetimeEnum.EPOCH)
print('NORMAL:', data)

data = orjson.dumps(DatetimeEnum.EPOCH, option=orjson.OPT_NAIVE_UTC)
print('   UTC:', data)
