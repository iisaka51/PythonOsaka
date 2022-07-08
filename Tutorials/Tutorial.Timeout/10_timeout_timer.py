from timeout_timer import timeout

@timeout(2):
def func():
    time.sleep(3)
    time.sleep(2)
