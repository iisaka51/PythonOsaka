import os
from invoke import Responder
from fabric2 import Connection

user = 'webapp'
password = os.environ.get('SUDO_PASSWORD')

c = Connection('webapp@web.example.com')
sudopass = Responder(
    pattern=rf'\[sudo\] password for {user}:',
    response=f'{password}\n',
)
c.run('sudo whoami', pty=True, watchers=[sudopass])
