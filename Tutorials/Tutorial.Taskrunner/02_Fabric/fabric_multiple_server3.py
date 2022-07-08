from fabric2 import Connection

servers = ('webapp@web1', 'webapp@web2')

def upload_and_cat(c, filename, remote_dir='/tmp'):
    if c.run('test -f /tmp/dummy.txt', warn=True).failed:
        c.put(filename, remote_dir)
        c.run(f'cat {remote_dir}/{filename}')

for host in servers:
    c = Connection(host)
    upload_and_cat(c, 'dummy.txt')
