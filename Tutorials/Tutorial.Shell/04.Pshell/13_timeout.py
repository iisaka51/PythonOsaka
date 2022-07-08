import pshell as sh
from subprocess import TimeoutExpired

try:
    sh.call('sleep 10', timeout=5)
except TimeoutExpired as e:
    print(f'Timeoout: {e}')
except:
    print('unknown')
print('done')
