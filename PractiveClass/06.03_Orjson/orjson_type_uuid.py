import orjson, uuid

data = orjson.dumps(uuid.UUID('f81d4fae-7dec-11d0-a765-00a0c91e6bf6'))
print(data)

data =  orjson.dumps(uuid.uuid5(uuid.NAMESPACE_DNS, "python.org"))
print(data)

