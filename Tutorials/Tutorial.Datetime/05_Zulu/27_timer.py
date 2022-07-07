import zulu

timer = zulu.Timer()
v1 = timer.start()
# <zulu.timer.Timer at 0x7fdb0e0b6180>

v2 = timer.started()
assert v2 == True

v3 = timer.stopped()
assert v3 == False

v4 = timer.elapsed()
# 0.0001289844512939453

v5 = timer.stop()
# <zulu.timer.Timer at 0x7fb17f63b300>

v6 = timer.elapsed()
# 0.0001499652862548828
