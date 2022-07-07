from cerberus import Validator

schema = {'name': {'type': 'string'},
           'age': {'type': 'integer', 'max': 45 }}

documents = [
  { 'name': 'David', 'age': 70 },
  { 'name': 'Brian', 'age': 75 },
  { 'name': 'Roger', 'age': 75 },
  { 'name': 'Jack', 'age': 51 },
  { 'name': 'Anthony', 'age': 29 },
  { 'name': 'Chloe', 'age': 28 },
]

v = Validator(schema)
valid_docs = [x for x in [v.validated(y) for y in documents]
                    if x is not None]

print(valid_docs)
