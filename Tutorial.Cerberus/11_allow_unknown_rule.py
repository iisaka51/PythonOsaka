from cerberus import Validator

v = Validator()
assert v.allow_unknown == False

schema = {
  'name': {'type': 'string'},
  'a_dict': {
    'type': 'dict',
    'allow_unknown': True,  # 注目：この定義でプロパティを上書きする
    'schema': {
      'address': {'type': 'string'}
    }
  }
}

document = {'name': 'john',
            'a_dict': {'an_unknown_field': 'is allowed'}}
c1 = (v.validate(document, schema), v.errors)
assert c1[0] == True

document = {'name': 'john',
            'an_unknown_field': 'is not allowed',
            'a_dict': {'an_unknown_field': 'is allowed'}}
c2 = (v.validate(document, schema), v.errors)
assert c2[0] == False
assert c2[1] == {'an_unknown_field': ['unknown field']}
