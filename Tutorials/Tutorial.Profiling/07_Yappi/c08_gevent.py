import yappi
from greenlet import greenlet
import time

class GreenletA(greenlet):
    def run(self):
        time.sleep(1)

yappi.set_context_backend("greenlet")
yappi.set_clock_type("wall")

yappi.start(builtins=True)
a = GreenletA()
a.switch()
yappi.stop()

yappi.get_func_stats().print_all()
