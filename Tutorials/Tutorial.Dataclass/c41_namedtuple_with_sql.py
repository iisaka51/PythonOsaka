from typing import NamedTuple
import sqlite3 as sqlite

class User(NamedTuple):
    id: int
    name: str
    part: str
    email: str

conn = sqlite.connect('user.db')

with conn:
    cur = conn.cursor()
    cur.execute('SELECT * FROM User')

    for user in map(User._make, cur.fetchall()):
        print(user)
