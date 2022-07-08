from fabric2 import Connection

result = Connection('web.example.com', user='webapp').run('uname -s', hide=True)
msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
print(msg.format(result))
