from cerberus import Validator

schema = {'name': {'type': 'string', 'maxlength': 10}}

documents = [
   {'name': 'Jack Bauer'},
   {'name': 'David Coverdale'},
   {'name': 77},
]

v = Validator(schema)

valid_docs = [x for x in [v.validated(y) for y in documents]
                 if x is not None]

c1 = (v.validate(documents[0]), v.errors)
assert c1[0] == True

c2 = (v.validate(documents[1]), v.errors)
assert c2[0] == False
assert c2[1] == {'name': ['max length is 10']}

c3 = (v.validate(documents[2]), v.errors)
assert c3[0] == False
assert c3[1] == {'name': ['must be of string type']}

print(f'Valid_docs: {valid_docs}')
