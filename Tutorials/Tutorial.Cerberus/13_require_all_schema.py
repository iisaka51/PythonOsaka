from cerberus import Validator

v = Validator()
assert v.require_all == False

schema = {
  'name': {'type': 'string'},
  'a_dict': {
    'type': 'dict',
    'require_all': True,  # 注目：この定義でプロパティを上書きする
    'schema': {
      'address': {'type': 'string'}
    }
  }
}

document = {'name': 'john', 'a_dict': {}}
c1 = (v.validate(document, schema), v.errors)
assert c1[0] == False
assert c1[1] == {'a_dict': [{'address': ['required field']}]}

document = {'a_dict': {'address': 'foobar'}}
c2 = (v.validate(document, schema), v.errors)
assert c2[0] == True
