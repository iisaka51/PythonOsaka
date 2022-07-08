from itertools import count
from pipe import select, take_while

euler1 = (
    sum(count()
        | select(lambda x: x * 3)
        | take_while(lambda x: x < 1000))
    + sum(count()
        | select(lambda x: x * 5)
        | take_while(lambda x: x < 1000))
    - sum(count()
        | select(lambda x: x * 15)
        | take_while(lambda x: x < 1000))
)

assert euler1 == 233168
