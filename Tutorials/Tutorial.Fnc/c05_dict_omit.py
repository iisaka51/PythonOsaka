import fnc

data = { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 }

v1 = fnc.mappings.pick(["name"], data)
v2 = fnc.mappings.omit(["abv"], data)

# v1
# v2
