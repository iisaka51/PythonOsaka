USER_ID=0
USER_NAME=1
USER_EMAIL=2

user = (1, 'Freddie', 'freddie@example.com')

# user
# user[USER_NAME]

from enum import Enum

class UserKey(Enum):
    USER_ID = 0
    USER_NAME=1
    USER_EMAIL=2

user[UserKey.USER_NAME.value]
