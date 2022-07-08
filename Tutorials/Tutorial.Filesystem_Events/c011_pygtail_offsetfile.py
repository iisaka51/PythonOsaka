import sys
from pygtail import Pygtail

for line in Pygtail('junk', offset_file='/tmp/junk.offset'):
    sys.stdout.write(line)
