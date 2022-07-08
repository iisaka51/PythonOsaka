from pipe import select, dedup, where

# ABV: Alcohol by Volume (アルコール度数)
beers = [
    { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 },
    { 'name': 'Pale Ale', 'abv': 6.0, 'stock': 0 },
    { 'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6 },
    { 'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24 },
    { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
]

v1 = list( beers | dedup(key=lambda beer: beer["name"]) )
v2 = list( beers
           | dedup(key=lambda beer: beer["name"])
           | select(lambda beer: beer["stock"]) )
v3 = list( beers
           | dedup(key=lambda beer: beer["name"])
           | select(lambda beer: beer["stock"])
           | where(lambda stock: stock > 10))

# v1
# v2
# v3
