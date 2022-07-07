from cerberus import Validator

schema = {'foo': {'rename': 'bar'}}
v = Validator(schema)

document = {'foo': 0}
c = v.normalized(document)

keys = c.keys()
assert ('foo' in keys) == False
assert ('bar' in keys) == True
assert c != document
assert c == {'bar': 0}
