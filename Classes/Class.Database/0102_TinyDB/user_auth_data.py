user_data = [
    { 'name': 'John',
      'group': ['user', 'operator', 'admin'],
    },
    { 'name': 'Freddie',
      'group': ['user','operator'],
    },
    { 'name': 'Brian',
      'group': ['user'],
    },
    { 'name': 'Roger',
      'group': ['user']
    },
]

group_data = [
    { 'name': 'user',
      'permission': [{'type': 'read'}]
    },
    { 'name': 'operator',
      'permission': [{'type': 'read'}, {'type': 'sudo'}]
    },
    { 'name': 'admin',
      'permission': [{'type': 'read'}, {'type': 'sudo'}, {'type': 'write'}]
    }
]

