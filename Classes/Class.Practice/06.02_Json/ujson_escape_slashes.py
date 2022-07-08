import ujson as json

data = "http://www.google.com"
serialized = json.dumps(data)
print(serialized)

serialized = json.dumps(data, escape_forward_slashes=False)
print(serialized)
