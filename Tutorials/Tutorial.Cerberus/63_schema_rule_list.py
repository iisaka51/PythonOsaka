from cerberus import Validator

schema = {'a_list': {'type': 'list',
                     'schema': {'type': 'integer'}}}

v = Validator(schema)

document = {'a_list': [3, 4, 5]}
c = v.validate(document)
assert c == True
