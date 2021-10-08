from cerberus import Validator, DocumentError

schema = {'name': {'type': 'string'},
           'age': {'type': 'integer', 'min': 10}}
document = {'name': 'Little Joe', 'age': 5}

v = Validator()
doc = f'{document}'

try:
    c  = (v.validate(doc, schema), v.errors)
except DocumentError as e:
    print(e)
