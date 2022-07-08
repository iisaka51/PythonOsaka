from fabric2 import Connection

servers = ('webapp@web1', 'webapp@web2')

for host in servers:
    c = Connection(host)
    if c.run('test -f /tmp/dummy.txt', warn=True).failed:
        c.put('dummy.txt', '/tmp')
        c.run('cat /tmp/dummy.txt')
