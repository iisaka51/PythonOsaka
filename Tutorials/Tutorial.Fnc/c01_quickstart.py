import fnc

# Arrays

data = [1, 2, [3, [4, 5, [6, 7]]]]
v1 = fnc.sequences.flatten(data)
assert list(v1) == [1, 2, 3, [4, 5, [6, 7]]]

v2 = fnc.sequences.flattendeep(data)
assert list(v2) == [1, 2, 3, 4, 5, 6, 7]

# Collections
data = [
   {'name': 'moe', 'age': 40},
   {'name': 'larry', 'age': 50},
   ]

v3 =  fnc.map('name', data)
assert list(v3) == ['moe', 'larry']

## Functions
curried = fnc.iteratee(lambda a, b, c: a + b + c)
v4 = curried(1, 2, 3)
assert v4 == 6

# Objects
data = {'name': 'moe', 'age': 40}
v5 = fnc.mappings.pick(['age'], data)
assert v5 == {'age': 40}
v6 = fnc.mappings.omit(['age'], data)
assert v6 == {'name': 'moe'}

# Utilities
v7 = list()
@fnc.retry(attempts=3, delay=0)
def do_something(seq):
    seq.append(len(seq))
    raise Exceptions('retry count exceeded')

try: do_something(v7)
except Exception: pass
assert v7 == [0, 1, 2]

# Compose like Chaining
data = [1, 2, 3, 4]
from functools import partial
do_without = partial(fnc.sequences.without, [2, 3])
do_reject = partial(fnc.sequences.reject, lambda x: x > 1)
do_without_reject = fnc.compose(
     do_without,
     do_reject
     )
v8 = do_without_reject(data)
assert list(v8) == [1]
