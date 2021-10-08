from cerberus import Validator

schema = {'name': {'type': 'string'},
           'age': {'type': 'integer', 'min': 10}}
document = {'name': 'Little Joe', 'age': 5}

v = Validator()
c  = (v.validate(document, schema), v.errors)

assert c[0] == False
assert c[1] == {'age': ['min value is 10']}

# v.validation_rules
