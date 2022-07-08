import getpass
from fabric2 import Connection, Config

sudo_pass = getpass.getpass("What's your sudo password?")
config = Config(overrides={'sudo': {'password': sudo_pass}})
c = Connection('webapp@web.example.com', config=config)
c.sudo('whoami', hide='stderr')
