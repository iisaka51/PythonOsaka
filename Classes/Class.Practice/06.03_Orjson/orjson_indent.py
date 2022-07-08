import orjson

data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
print('DATA:', repr(data))

normal = orjson.dumps(data)
indent_bytes = orjson.dumps(data, option=orjson.OPT_INDENT_2)

print('NORMAL:', normal)
print('INDENT bytes:', indent_bytes)
print('INDENT str:', indent_bytes.decode())
