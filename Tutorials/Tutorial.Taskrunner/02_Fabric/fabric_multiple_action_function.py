from fabric2 import Connection

def upload_and_cat(c, filename, remote_dir='/tmp'):
    c.put(filename, remote_dir)
    c.run(f'cat {remote_dir}/{filename}')


c = Connection('webapp@web.example.com')
upload_and_cat(c, 'dummy.txt')
