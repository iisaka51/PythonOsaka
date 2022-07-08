import fnc

beers = [
    { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 },
    { 'name': 'Pale Ale', 'abv': 6.0, 'stock': 0 },
    { 'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6 },
    { 'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24 },
    { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
]

pilserl = lambda x: x["name"] == "Pilserl"
paleale = lambda x: x["name"] == "Pale Ale"
yebisu = lambda x: x["name"] == "YEBISU"
v1 = fnc.sequences.findindex(pilserl, beers)
v2 = fnc.sequences.findindex(paleale, beers)
v3 = fnc.sequences.findindex(yebisu, beers)

# v1
# v2
# v3
