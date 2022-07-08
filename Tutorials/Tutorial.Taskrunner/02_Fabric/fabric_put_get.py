from fabric2 import Connection

conn = Connection('webapp@web.example.com')

# result = conn.put(local='./dummy.txt', remote='/tmp/')
result = conn.put('./dummy.txt', remote='/tmp/')
print("Uploaded {0.local} to {0.remote}".format(result))

# result = conn.get(remote='/tmp/dummy.txt', local='./junk.txt')
result = conn.get('/tmp/dummy.txt', local='./junk.txt')
print("Download {0.local} to {0.remote}".format(result))
