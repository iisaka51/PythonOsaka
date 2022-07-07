import zulu
import time

timer = zulu.Timer()

with timer:
    time.sleep(1)

# これは次と同じこと
with zulu.Timer() as timer:
    time.sleep(1)

v1 = timer.elapsed()
# 1.0052082538604736

# 複数回使用して持続時間を蓄積できる
with timer:
    time.sleep(2)

v2 = timer.elapsed()
# 3.0064713954925537

# タイマーのリセット
v3 = timer.reset()
# <zulu.timer.Timer at 0x7fa53c185140>

v4 = timer.started()
assert v4 == False

v5 = timer.elapsed()
# 0
