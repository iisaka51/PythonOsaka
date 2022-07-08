import pydash as py_

beers = [
    { 'name': 'Pale Ale',
      'attributes': { 'abv': 6.0, 'stock': 0 }},
    { 'name': 'ICHII SENSHIN',
      'attributes': { 'abv': 6.5, 'stock': 6 }},
    { 'name': 'ICHIGO ICHIE',
      'attributes': { 'abv': 5.5, 'stock': 24 }},
    { 'name': 'Pilserl',
      'attributes': { 'abv': 4.9, 'stock': 12 }},
]

v1 = py_.map_(beers, "attributes.abv" )

# v1

