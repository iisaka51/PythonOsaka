from shell import shell, Shell

_MSG_='Hello World!'
v1 = shell('cat -u', has_input=True).write(_MSG_).output()
v2 = Shell(has_input=True).run('cat -u').write(_MSG_).output()

# print(v1)
# print(v2)
