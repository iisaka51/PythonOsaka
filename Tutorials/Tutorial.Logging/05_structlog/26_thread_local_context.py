from structlog.threadlocal import wrap_dict

WrappedDictClass = wrap_dict(dict)

d1 = WrappedDictClass({"a": 1})
d2 = WrappedDictClass({"b": 2})
d3 = WrappedDictClass()

v1 = d3["c"] = 3
v2 = d1 is d3
v3 = d1 == d2 == d3 == WrappedDictClass()

# print(v1)
# print(v2)
# print(v3)
# print(d3)
