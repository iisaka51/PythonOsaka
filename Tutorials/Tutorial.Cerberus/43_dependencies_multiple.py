from cerberus import Validator

schema = {'field1': {'required': False},
          'field2': {'required': False},
          'field3': {'required': False,
                     'dependencies': ['field1', 'field2']}}

v = Validator()

document = {'field1': 7, 'field2': 11, 'field3': 13}
c = v.validate(document, schema)
assert c == True

document = {'field2': 11, 'field3': 13}
c = v.validate(document, schema)
assert c == False
assert v.errors == {'field3': ["field 'field1' is required"]}
