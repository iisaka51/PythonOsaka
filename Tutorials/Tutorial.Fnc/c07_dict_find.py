import fnc

beers = [
    { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 },
    { 'name': 'Pale Ale', 'abv': 6.0, 'stock': 0 },
    { 'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6 },
    { 'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24 },
    { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
]

v1 = fnc.sequences.find({"name": "Pilserl"}, beers)
v2 = fnc.sequences.find({"name": "Pale Ale"}, beers)
v3 = fnc.sequences.find({"name": "YEBISU"}, beers)

# v1
# v2
# v3
