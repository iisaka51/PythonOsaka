import snoop
import random

def foo():
    lst = []
    for i in range(10):
        lst.append(random.randrange(1, 1000))

    with snoop:
        lower = min(lst)
        upper = max(lst)
        mid = (lower + upper) / 2

    return lower, mid, upper

# foo()
