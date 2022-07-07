from cerberus import Validator

schema = {'amount': {'type': 'integer'},
          'kind': {'type': 'string', 'default': 'purchase'}}
v = Validator(schema)

c1 = v.normalized({'amount': 1})
assert c1 == {'amount': 1, 'kind': 'purchase'}

c2 = v.normalized({'amount': 1, 'kind': None})
assert c2 == {'amount': 1, 'kind': 'purchase'}

c3 = v.normalized({'amount': 1, 'kind': 'other'})
assert c3 == {'amount': 1, 'kind': 'other'}
