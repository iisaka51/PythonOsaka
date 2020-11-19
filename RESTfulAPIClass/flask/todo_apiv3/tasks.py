from flask_restful import fields

task_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('task')
}

tasks = [
     {
         'id': 1,
         'title': 'Buy Beer',
         'description': 'IPA 6 bottles',
         'done': False
     },
     {
         'id': 2,
         'title': 'Buy groceries',
         'description': 'Beef, Tofu, Sting Onion',
         'done': False
     }
]

