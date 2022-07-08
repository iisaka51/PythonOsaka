from shell import shell, Shell

sh = shell('cat sample.txt', record_output=False, record_errors=False)
v1 = sh.code
v2 = sh.output()

sh = Shell(record_output=False, record_errors=False)
sh.run('cat sample.txt')
v3 = sh.code
v4 = sh.output()

# print(v1)
# ...
# print(v4)

