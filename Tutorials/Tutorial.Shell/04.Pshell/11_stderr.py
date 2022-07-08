import pshell as sh

with open('/tmp/cmderr.txt', 'w') as errfp:
    v1 = sh.call('ls /tmp/junk', stderr=errfp)

# print(v1)
# !cat /tmp/cmderr.txt
