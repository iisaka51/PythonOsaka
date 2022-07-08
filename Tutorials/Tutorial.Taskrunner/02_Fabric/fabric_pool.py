from fabric2 import SerialGroup as Group
from fabric2.transfer import Transfer

pool = Group('webapp@web1', 'webapp@web2')
conn = Transfer(pool)
conn.put('dummy.txt', '/tmp')
pool.run('cat /tmp/dummy.txt')
