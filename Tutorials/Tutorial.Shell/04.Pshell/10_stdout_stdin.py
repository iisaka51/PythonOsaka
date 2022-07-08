import pshell as sh

with open('sample.txt') as infp:
    with open('/tmp/cmdout.txt', 'w') as outfp:
        v1 = sh.call('cat', stdout=outfp, stdin=infp)

# print(v1)
# !cat /tmp/cmdout.txt
