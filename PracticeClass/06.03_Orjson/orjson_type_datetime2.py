import orjson, datetime

data = orjson.dumps(datetime.time(12, 0, 15, 290))
print(' TIME:', data)

data = orjson.dumps(datetime.date(2021, 1, 2))
print(' DATE:', data)


