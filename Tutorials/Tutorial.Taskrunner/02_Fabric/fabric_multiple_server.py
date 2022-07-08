from fabric2 import Connection

for host in ('webapp@web1', 'webapp@web2'):
    result = Connection(host).run('uname -s')
    print("{}: {}".format(host, result.stdout.strip()))
