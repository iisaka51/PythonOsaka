import pydash as py_

data = [[1, 2], [3, [4, 5]]]

v1 = py_.flatten(data)
v2 = py_.flatten_deep(data)

# v1
# v2
