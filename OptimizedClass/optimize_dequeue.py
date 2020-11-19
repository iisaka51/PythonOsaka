import sys
from array import array
from benchmarker import Benchmarker
from collections import deque

n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000*1000
print(n)
with Benchmarker(n, width=20) as bench:
    nay = []
    iay = array('I', [])
    day = deque()

    @bench("list")
    def _(bm):
        for i in range(n):
            nay.insert(0, i)

    @bench("array")
    def _(bm):
        for i in range(n):
            iay.insert(0, i)

    @bench("deque")
    def _(bm):
        for i in bm:
          day.appendleft( i )
