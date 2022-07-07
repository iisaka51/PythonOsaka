from cerberus import Validator

schema = {'field1': {'required': False},
          'field2': {'required': False,
                     'dependencies': 'field1'}}

v = Validator()

document = {'field1': 7}
c1 = v.validate(document, schema)
assert c1 == True

document = {'field2': 7}
c2 = v.validate(document, schema)
assert c2 == False
assert v.errors == {'field2': ["field 'field1' is required"]}
