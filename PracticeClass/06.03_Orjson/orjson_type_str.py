import orjson, ujson, json

try:
    data = orjson.dumps('\ud800')
except orjson.JSONEncodeError as msg:
    print('orjson JSONEncodeError:', msg)

try:
    data = ujson.dumps('\ud800')
except UnicodeEncodeError as msg:
    print('ujson UnicodeEncodeError:', msg)

data = json.dumps('\ud800')
print('json dumps():', data)

try:
    data = orjson.loads('"\\ud800"')
except orjson.JSONDecodeError as msg:
    print('orjson JSONDecodeError:', msg)

data = ujson.loads('"\\ud800"')
print('ujson loads():{!r}'.format(data))

data = json.loads('"\\ud800"')
print('json loads():{!r}'.format(data))
