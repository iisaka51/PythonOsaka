import zulu
import time

# 最大15秒のつタイマー
timer = zulu.Timer(timeout=15)
v1 = timer.start()
# <zulu.timer.Timer at 0x7fa8c0b8bf80>

v2 = timer.done()
assert v2 == False

v3 = timer.remaining()
# 14.999913930892944

time.sleep(5)

v4 = timer.remaining()
# 9.99487590789795

time.sleep(10)

v5 = timer.done()
assert v5 == True

v6 = timer.remaining()
# -0.009467124938964844

v7 = timer.start()
# <zulu.timer.Timer at 0x7fa8c0b8bf80>

v8 = timer.done()
assert v8 == False
