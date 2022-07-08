from bash import bash
from subprocess import TimeoutExpired

try:
    bash('sleep 10', timeout=5)
except TimeoutExpired as e:
    print(f'Timeoout: {e}')
except:
    print('unknown')
print('done')
