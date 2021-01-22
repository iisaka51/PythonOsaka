import orjson, ujson, json

data = orjson.dumps([float("NaN"), float("Infinity"), float("-Infinity")])
print('orjson:', data)

data = ujson.dumps([float("NaN"), float("Infinity"), float("-Infinity")])
print('ujson:', data)

data = json.dumps([float("NaN"), float("Infinity"), float("-Infinity")])
print('json:', data)
