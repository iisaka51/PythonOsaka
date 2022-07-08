from structlog.threadlocal import wrap_dict

WrappedDictClass = wrap_dict(dict)
AnotherWrappedDictClass = wrap_dict(dict)

v1 = WrappedDictClass() != AnotherWrappedDictClass()
v2 = WrappedDictClass.__name__
v3 = AnotherWrappedDictClass.__name__

# print(v1)
# print(v2)
# print(v3)
