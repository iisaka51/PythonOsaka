import orjson

data = orjson.dumps([])
print(data)

data = orjson.dumps([], option=orjson.OPT_APPEND_NEWLINE)
print(data)
