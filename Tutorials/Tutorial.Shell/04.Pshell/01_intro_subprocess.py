import pshell as sh
import subprocess
import shlex

cmd = 'ls /tmp'
v1 = subprocess.call(shlex.split(cmd))
# print(v1)
