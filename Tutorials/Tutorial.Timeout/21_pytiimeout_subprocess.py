import timeout
import time

@timeout.timeout(duration=5)
def foo() -> None:
    while True:
        time.sleep(1)

try:
    foo()
except timeout.TimeoutException:
    pass
