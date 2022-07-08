import ZODB.utils
import ZODB.TimeStamp
from fake_time import *

tid1 = ZODB.utils.newTid(None)
tid2 = ZODB.utils.newTid(tid1)

v1  = ZODB.TimeStamp.TimeStamp(tid1)
v2  =  ZODB.utils.u64(tid1), ZODB.utils.u64(tid2)

# print(tid1)
# print(tid2)
# print(v1)
# print(v2)
