from bash import bash

with open('/tmp/current_time.txt', 'w') as fp:
    bash("date", stdout=fp)

#!cat /tmp/current_time.txt
