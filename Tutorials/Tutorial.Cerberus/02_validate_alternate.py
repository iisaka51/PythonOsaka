from cerberus import Validator

schema = {'name': {'type': 'string'}}
document = {'name': 'Jack Bauer'}

v = Validator()
check = v.validate(document, schema)
assert check == True

# v.types
