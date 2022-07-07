from cerberus import Validator

schema1 = {'prop1': {'type': 'number', 'min':   0, 'max':  10}}
schema2 = {'prop1': {'type': 'number', 'min': 100, 'max': 110}}

v = Validator()

document = {'prop1': 5}
c = v.validate(document, schema1) or v.validate(document, schema2)
assert c == True

document = {'prop1': 105}
c = v.validate(document, schema1) or v.validate(document, schema2)
assert c == True

document = {'prop1': 55}
c = v.validate(document, schema1) or v.validate(document, schema2)
assert c == False
assert v.errors == {'prop1': ['min value is 100']}
