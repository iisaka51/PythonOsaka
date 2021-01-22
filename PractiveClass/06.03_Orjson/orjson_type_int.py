import orjson

data = orjson.dumps(9007199254740992)
print(data)

try:
    data = orjson.dumps(9007199254740992,
                        option=orjson.OPT_STRICT_INTEGER)
except orjson.JSONEncodeError as msg:
    print('JSONEncodeError:', msg)

try:
    data = orjson.dumps(-9007199254740992,
                        option=orjson.OPT_STRICT_INTEGER)
except orjson.JSONEncodeError as msg:
    print('JSONEncodeError:', msg)
