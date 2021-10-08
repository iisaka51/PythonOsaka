from cerberus import Validator

schema = {'field1': {'required': False},
          'field2': {'required': True,
                     'dependencies': {'field1': ['one', 'two']}}}

v = Validator()

document = {'field1': 'one', 'field2': 7}
c = (v.validate(document, schema), v.errors)
assert c[0] == True

document = {'field1': 'three', 'field2': 7}
c = (v.validate(document, schema), v.errors)
assert c[0] == False
assert c[1] == {'field2':
               ["depends on these values: {'field1': ['one', 'two']}"]}

# dependencies のリストを使うのと同じ
document = {'field2': 7}
c = (v.validate(document, schema), v.errors)
assert c[0] == False
assert c[1] == {'field2':
                ["depends on these values: {'field1': ['one', 'two']}"]}

# 単一のdependencies を渡すこともできます。
schema = {'field1': {'required': False},
          'field2': {'dependencies': {'field1': 'one'}}}
document = {'field1': 'one', 'field2': 7}
c = (v.validate(document, schema), v.errors)
assert c[0] == True

document = {'field1': 'two', 'field2': 7}
c = (v.validate(document, schema), v.errors)
assert c[0] == False
assert c[1] == {'field2':
                ["depends on these values: {'field1': 'one'}"]}

