import orjson

class Secret(str):
    pass

def custom_type(obj):
    if isinstance(obj, Secret):
        return "******"
    raise TypeError

sec_obj = Secret("zxc")
data = orjson.dumps(sec_obj)
print('  DATE:', data)
print('NORMAL:', data)

try:
    data =  orjson.dumps(
                sec_obj,
                option=orjson.OPT_PASSTHROUGH_SUBCLASS)
except TypeError as msg:
    print('ERROR:', msg)

data = orjson.dumps(
            sec_obj,
            option=orjson.OPT_PASSTHROUGH_SUBCLASS,
            default=custom_type)
print('CUSTOM:', data)
