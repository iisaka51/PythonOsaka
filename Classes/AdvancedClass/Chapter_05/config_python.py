import sys
from pathlib import Path

homedir = Path.home() / '.myapp'
sys.path.insert(0, str(homedir))

import config

print('dbhost => ', config.dbhost)
print('  user => ', config.user)
print('passwd => ', config.passwd)
print('dbname => ', config.dbname)
