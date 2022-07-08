from bash import bash

with open('/tmp/error.txt', 'w') as fp:
    bash("ls -l /tmp/dummyfile", stderr=fp)

#!cat /tmp/error.txt
