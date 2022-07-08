import pshell as sh
from subprocess import CalledProcessError

try:
    sh.check_call('ls /tmp/missing_file')
except CalledProcessError as e:
    print(f'Error: {e}')
