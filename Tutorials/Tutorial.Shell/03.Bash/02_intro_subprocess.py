import subprocess
import shlex

cmdline = 'ls /tmp'

ls = subprocess.run(shlex.split(cmdline),
                       encoding='utf-8', stdout=subprocess.PIPE)
for file in ls.stdout.splitlines():
    print(file)

