from cerberus import Validator

schema = {'quotes': {'type': ['string', 'list']}}
v = Validator()

document = {'quotes': 'Hello world!'}
c = v.validate(document, schema)
assert c == True

document = {'quotes': ['Do not disturb my circles!', 'Heureka!']}
c = v.validate(document, schema)
assert c == True

schema = {'quotes': {'type': ['string', 'list'],
                     'schema': {'type': 'string'}}}

document = {'quotes': 'Hello world!'}
c = v.validate(document, schema)
assert c == True

document = {'quotes': [1, 'Heureka!']}
c = (v.validate(document, schema), v.errors)
assert c[0] == False
assert c[1] == {'quotes': [{0: ['must be of string type']}]}
