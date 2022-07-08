from model_sqldemo import *

v1 = backend.filter(Beer, {})

def show(data):
    for d in data:
        print(f'{d.name} {d.abv}')

# show(v1)
