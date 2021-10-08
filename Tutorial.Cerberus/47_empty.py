from cerberus import Validator

schema = {'name': {'type': 'string', 'empty': False}}
document = {'name': ''}

v = Validator()
c = (v.validate(document, schema), v.errors)
assert c[0] == False
assert c[1] == {'name': ['empty values not allowed']}
