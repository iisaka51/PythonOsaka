import orjson, datetime

date_obj = datetime.datetime(2021, 1, 1, 0, 0, 0),

json_data = orjson.dumps(date_obj)
print('NORMAL    :', json_data)

json_data = orjson.dumps(date_obj, option=orjson.OPT_NAIVE_UTC)
print('NATIVE_UTC:', json_data)
