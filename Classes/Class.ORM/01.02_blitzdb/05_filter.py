from model_beerdb import *

v1 = backend.filter(Beer, {'abv' : 5.5})

def show(data):
    for d in data:
        print(f'{d.name} {d.abv}')

# pirnt(v1)
# show(v1)
