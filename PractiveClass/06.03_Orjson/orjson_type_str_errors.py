import orjson

try:
    data = orjson.loads(b'"\xed\xa0\x80"')
except orjson.JSONDecodeError as msg:
    print('JSONDecodeError:', msg)

data = orjson.loads(b'"\xed\xa0\x80"'.decode("utf-8", "replace"))
print('decoded:', data)
