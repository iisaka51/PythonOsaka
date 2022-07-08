from bash import bash

# ls -l /etc/ | wc -l
v1 = bash('ls -l /etc/ | wc -l').value()
v2 = bash('ls -l /etc/').bash('wc -l').value()

# print(v1)
# print(v2)
