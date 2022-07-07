from cerberus import Validator

schema = {'name': {'type': 'string'}}
document = {'name': 'Jack Bauer'}

v = Validator(schema)
check = v.validate(document)
assert check == True
