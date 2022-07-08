from bash import bash

ls = bash('ls /tmp')
for file in ls.value().splitlines():
    print(file)
