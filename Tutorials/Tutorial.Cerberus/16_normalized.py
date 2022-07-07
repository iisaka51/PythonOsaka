from cerberus import Validator

schema = {'amount': {'coerce': int}}
document = {'model': 'consumerism', 'amount': '1'}

v = Validator()
normalized_document = v.normalized(document, schema)
assert normalized_document == {'model': 'consumerism', 'amount': 1}
assert type(normalized_document['amount']) == int
