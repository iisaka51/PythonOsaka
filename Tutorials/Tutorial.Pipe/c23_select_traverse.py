from pipe import select, traverse

# ABV: Alcohol by Volume (アルコール度数)
beers = [
    { 'name': 'Pale Ale', 'abv': [5.5, 6.0], 'stock': 6 },
    { 'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6 },
    { 'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24 },
    { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
]

v1 = list( beers
             | select(lambda x: x["abv"])
             | traverse)

# v1
