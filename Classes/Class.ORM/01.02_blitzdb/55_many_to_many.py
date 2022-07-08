from model_sqldemo3 import *
from pprint import pprint

plank = backend.get(Brewery, {'name': 'Plank'})
pilserl = backend.get(Beer, {'name': 'Pilserl'})

pilserl.brewery = plank
plank.product = pilserl

# pprint(pilserl)
# pprint(plank)
# print(pilserl.brewery.country)
# print(plank.product)
