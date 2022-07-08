import time

# time.time() が同じ値を返すようにするハック
old_time = time.time
def fake_time():
    return 1224825068.12

time.time = fake_time
