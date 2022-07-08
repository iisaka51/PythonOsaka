import pydash as py_

# Arrays

data = [1, 2, [3, [4, 5, [6, 7]]]]
v1 = py_.flatten(data)
assert v1 == [1, 2, 3, [4, 5, [6, 7]]]

v2 = py_.flatten_deep(data)
assert v2 == [1, 2, 3, 4, 5, 6, 7]

# Collections
data = [
   {'name': 'moe', 'age': 40},
   {'name': 'larry', 'age': 50},
   ]

v3 =  py_.map_(data, 'name')
assert v3 == ['moe', 'larry']

# Functions
curried = py_.curry(lambda a, b, c: a + b + c)
v4 = curried(1, 2)(3)
assert v4 == 6

# Objects
data = {'name': 'moe', 'age': 40}
v5 = py_.omit(data, 'age')
assert v5 == {'name': 'moe'}

# Utilities
v6 = py_.times(3, lambda index: index)
assert v6 == [0, 1, 2]

# Chaining
v7 = ( py_.chain([1, 2, 3, 4])
       .without(2, 3)
       .reject(lambda x: x > 1)
       .value() )
assert v7 == [1]
