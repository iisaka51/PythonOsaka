import ujson as json

data = [{'a': 'A', 'b': (2, 4),   'c': 3.0}]
sirialized_data = json.dumps(data)
print(sirialized_data)

new_data = json.loads(sirialized_data)
print(new_data)

