from sh import ls
import shlex

cmd = "ls -l /tmp/dummyfile"
v1 = ls(shlex.split(cmd)[1:])

# print(v1)
