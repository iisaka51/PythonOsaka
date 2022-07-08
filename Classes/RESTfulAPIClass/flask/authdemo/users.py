class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'freddie', 'queen'),
]

username_table = {user.username: user for user in users}
userid_table = {user.id: user for user in users}
