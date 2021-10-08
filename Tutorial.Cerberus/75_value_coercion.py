from cerberus import Validator

v = Validator()
v.schema = {'amount': {'type': 'integer'}}
c = v.validate({'amount': '1'})
assert c == False

v.schema = {'amount': {'type': 'integer', 'coerce': int}}
c = v.validate({'amount': '1'})
assert c == True
assert v.document == {'amount': 1}

to_bool = lambda v: v.lower() in ('true', '1')
v.schema = {'flag': {'type': 'boolean', 'coerce': (str, to_bool)}}
c = v.validate({'flag': 'true'})
assert c == True
assert v.document == {'flag': True}
