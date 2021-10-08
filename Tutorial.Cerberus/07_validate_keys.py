from cerberus import Validator

schema = {'name': {'type': 'string'},
           'age': {'type': 'integer', 'min': 10}}
doc1 = {'name': 'David Coverdale'}
doc2 = {'name': 'David Coverdale', 'country': 'USA'}

v = Validator(schema)
c1 = (v.validate(doc1), v.errors)
assert c1[0] == True
assert c1[1] == {}

c2 = (v.validate(doc2), v.errors)
assert c2[0] == False
assert c2[1] == {'country': ['unknown field']}
