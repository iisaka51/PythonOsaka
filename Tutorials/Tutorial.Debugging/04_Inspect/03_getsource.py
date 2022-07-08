import inspect
from ackermann import ackermann

_ = ackermann(3, 10)

src = inspect.getsource(ackermann)
print(src)
