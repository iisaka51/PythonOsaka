import sys
from pygtail import Pygtail

for line in Pygtail('junk'):
    sys.stdout.write(line)
