from cerberus import Validator

schema = {'this_field': {'type': 'dict',
                         'excludes': 'that_field',
                         'required': True},
          'that_field': {'type': 'dict',
                         'excludes': 'this_field',
                         'required': True}
        }

v = Validator(schema)
document = {'this_field': {}, 'that_field': {}}
c1 = (v.validate(document), v.errors)
assert c1[0] == False
assert c1[1] == {'that_field':
                 ["'this_field' must not be present with 'that_field'"],
                 'this_field':
                 ["'that_field' must not be present with 'this_field'"]}

document = {'this_field': {}}
c2 = (v.validate(document), v.errors)
assert c2[0] == True

document = {'that_field': {}}
c3 = (v.validate(document), v.errors)
assert c3[0] == True

document = {}
c4 = (v.validate(document), v.errors)
assert c4[0] == False
assert c4[1] == {'that_field': ['required field'],
                 'this_field': ['required field']}
