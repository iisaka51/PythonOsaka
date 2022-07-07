from cerberus import Validator

schema = {'name': {'type': 'string'}}
document = {'name': 12345 }

v = Validator()
check = v.validate(document, schema)

assert check == False
assert v.errors == {'name': ['must be of string type']}
