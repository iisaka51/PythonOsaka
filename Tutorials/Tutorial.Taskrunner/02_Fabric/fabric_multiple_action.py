from fabric2 import Connection
c = Connection('webapp@web.example.com')
c.put('dummy.txt', '/tmp')
c.run('cat /tmp/dummy.txt')

