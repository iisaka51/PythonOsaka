from model_strict import *

data = [
    { 'strict_bool': True },
    { 'strict_bool': False },
    { 'strict_bool': 'True' },
    { 'strict_bool': 'False' },
    { 'strict_bool': 1 },
    { 'strict_bool': 0 },
    { 'strict_bool': None },
]

def func():
    for d in data:
        try:
            flag = StrictBoolModel(**d)
        except ValidationError as e:
            flag = e
        val = d['strict_bool']
        print(f'{val}({type(val)}): {flag}')

# func()
