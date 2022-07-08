from fabric2 import Connection
c = Connection('webapp@web.example.com')
c.run('sudo id', pty=True)
