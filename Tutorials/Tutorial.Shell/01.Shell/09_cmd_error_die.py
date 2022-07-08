from shell import shell
ls = shell('ls /tmp/PythonOsaka', die=True)
if ls.code != 0:
    print(f'Error: {ls.errors()}')
