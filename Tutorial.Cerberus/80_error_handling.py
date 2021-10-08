from cerberus import Validator
from cerberus.errors import BAD_TYPE

schema = {'cats': {'type': 'integer'}}
document = {'cats': 'two'}

v = Validator()

c = v.validate(document, schema)
assert c == False
assert BAD_TYPE in v._errors

c = v.document_error_tree['cats'].errors
assert c == v.schema_error_tree['cats']['type'].errors

assert BAD_TYPE in v.document_error_tree['cats']

c = v.document_error_tree['cats'][BAD_TYPE]
assert c == v.document_error_tree['cats'].errors[0]

error = v.document_error_tree['cats'].errors[0]
assert error.document_path == ('cats',)
assert error.schema_path == ('cats', 'type')
assert error.rule == 'type'
assert error.constraint == 'integer'
assert error.value == 'two'
