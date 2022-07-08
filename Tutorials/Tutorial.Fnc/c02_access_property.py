import pydash as py_

data = [{'a.b': 1, 'a': {'b': 3}}, {'a.b': 2, 'a': {'b': 4}}]
v1 = py_.map_(data, ['a.b'])
# v1
