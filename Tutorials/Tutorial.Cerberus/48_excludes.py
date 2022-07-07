from cerberus import Validator

v = Validator()
schema = {'this_field': {'type': 'dict',
                         'excludes': 'that_field'},
          'that_field': {'type': 'dict',
                         'excludes': 'this_field'}}

c1 = (v.validate({'this_field': {}, 'that_field': {}}, schema), v.errors)
assert c1[0] == False
assert c1[1] == {'that_field':
                ["'this_field' must not be present with 'that_field'"],
                'this_field':
                ["'that_field' must not be present with 'this_field'"]}

c2 = v.validate({'this_field': {}}, schema)
assert c2 == True

c3 = v.validate({'that_field': {}}, schema)
assert c3 == True

c4 = v.validate({}, schema)
assert c4 == True
