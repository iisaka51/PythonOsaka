from model_sqldemo import *

v1 = backend.filter(Beer, {})

def show(data):
    try:
        for d in data:
            print(f'{d.name} {d.abv}')
    except RuntimeError:
        pass

# show(v1)
