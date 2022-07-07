from cerberus import Validator

schema = {'foo': {'type': 'string'}}
v = Validator(schema, purge_unknown=True)

c = v.normalized({'bar': 'foo'})
assert c == {}

c = v.normalized({'foo': 'bar'})
assert c == {'foo': 'bar'}
