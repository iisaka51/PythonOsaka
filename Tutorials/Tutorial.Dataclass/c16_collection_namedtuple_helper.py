from collections import namedtuple
import json

User = namedtuple("User", "id name email")

user = User(1, "Freddie", "freddie@example.com")

v1 = user
v2 = user._replace(id=2)
v3 = user._make([2, 'Brian', 'brian@example.com'])

v4 = user._asdict()
v5 = json.dumps(v4)
