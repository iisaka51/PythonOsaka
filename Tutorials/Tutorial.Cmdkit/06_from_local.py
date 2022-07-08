import os
from cmdkit.config import Configuration
from pprint import pprint

HOME, CWD = os.getenv('HOME'), os.getcwd()

cfg = Configuration.from_local(
            default=None, env=True, prefix='MYAPP',
            system='/etc/myapp.yml',
            user=f'{HOME}/.myapp.yml',
            local=f'{CWD}/myapp.yml')

# pprint(cfg)
