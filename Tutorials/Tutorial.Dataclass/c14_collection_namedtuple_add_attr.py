from collections import namedtuple

UserMixin = namedtuple("UserMixin", "id name email")
User = namedtuple( 'User', UserMixin._fields + ('grup',))
user = User(1, 'Freddie', 'freddie@example.com', 'Queeness')

# user
