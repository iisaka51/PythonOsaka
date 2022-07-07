from cerberus import Validator

schema = {'this_field': {'type': 'dict',
                         'excludes': ['that_field', 'bazo_field']},
          'that_field': {'type': 'dict',
                         'excludes': 'this_field'},
          'bazo_field': {'type': 'dict'}}

v = Validator(schema)

document = {'this_field': {}, 'bazo_field': {}}
c = (v.validate(document), v.errors)
assert c[0] == False
assert c[1] == {'this_field':
  ["'that_field', 'bazo_field' must not be present with 'this_field'"]}
