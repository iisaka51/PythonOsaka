from fabric2 import SerialGroup as Group

conn = Group('webapp@web1', 'webapp@web2')
results = con.run('uname -s')

for connection, result in results.items():
    print("{0.host}: {1.stdout}".format(connection, result))
