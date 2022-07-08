from shell import shell
ls = shell('ls /tmp/PythonOsaka')
if ls.code != 0:
    print(f'Error: {ls.errors()}')
