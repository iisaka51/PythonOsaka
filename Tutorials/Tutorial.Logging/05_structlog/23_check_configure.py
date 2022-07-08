import structlog
from pprint import pprint

class MyDict(dict):
    pass

v1 = structlog.is_configured()
v2 = structlog.configure(context_class=MyDict)
v3 = structlog.is_configured()

cfg = structlog.get_config()
v4 = cfg["context_class"]

# print(v1)
# print(v2)
# print(v3)
# pprint(cfg)
# print(v4)
