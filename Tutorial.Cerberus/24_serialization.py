import yaml
from cerberus import Validator

schema_text = '''
name:
  type: string
age:
  type: integer
  min: 10
'''

schema = yaml.load(schema_text, Loader=yaml.SafeLoader)
document = {'name': 'Little Joe', 'age': 5}

v = Validator(schema)
c = (v.validate(document), v.errors)
assert c[0] == False
assert c[1] == {'age': ['min value is 10']}
