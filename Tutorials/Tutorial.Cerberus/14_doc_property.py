from cerberus import Validator

v = Validator()
v.schema = {'amount': {'type': 'integer', 'coerce': int}}

document = {'amount': 1}
c = v.validate(document)
assert c == True
assert v.document == document
