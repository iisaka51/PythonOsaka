from cerberus import Validator

schemas = [
    {'department': {'required': True, 'regex': '^CTU$'},
     'phone': {'nullable': True} },
    {'department': {'required': True},
     'phone': {'required': True}}
  ]

employee_schema = {'employee': {'oneof_schema': schemas,
                                'type': 'dict'}}

employee_vldtr = Validator(employee_schema, allow_unknown=True)

employees = [
  { 'employee': { 'name': 'Jack Bauer',
                  'department': 'CTU', 'phone': None }},
  { 'employee': { 'name': "Chloe O'Brian",
                  'department': 'CTU', 'phone': '001022' }},
  { 'employee': { 'name': 'Anthony Tony',
                  'department': 'CTU', 'phone': '001023' }},
  { 'employee': { 'name': 'Ann Wilson',
                  'department': 'Heart', 'phone': '002001' }},
  { 'employee': { 'name': 'Nacy Wilson',
                  'department': 'Heart', 'phone': None }}
]

invalid_employees_phones = []
for employee in employees:
    if not employee_vldtr.validate(employee):
        invalid_employees_phones.append(employee)

from pprint import pprint as print
print(invalid_employees_phones)
