import orjson, decimal
def decimal_object(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError

try:
    orjson.dumps(decimal.Decimal("0.0842389659712649442845"))
except orjson.JSONEncodeError as msg:
    print(msg)

json_data = orjson.dumps(decimal.Decimal("0.0842389659712649442845"),
                         default=decimal_object)

try:
    json_data = orjson.dumps({1, 2}, default=decimal_object)
except TypeError as msg:
    print(msg)
