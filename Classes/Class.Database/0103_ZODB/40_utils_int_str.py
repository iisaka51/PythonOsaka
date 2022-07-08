import ZODB.utils

v1 = ZODB.utils.p64(12345678901234567890)
v2 = ZODB.utils.u64(b'\xabT\xa9\x8c\xeb\x1f\n\xd2')
v3 = ZODB.utils.z64

# print(v1)
# print(v2)
# print(v3)
