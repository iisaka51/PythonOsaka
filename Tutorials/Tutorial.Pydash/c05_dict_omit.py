import pydash as py_

data = { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 }

v1 = py_.omit(data, "name")

# v1
