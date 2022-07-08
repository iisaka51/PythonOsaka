from sh import ssh

myserver = ssh.bake("myserver.com", l='iisaka')

ls = myserver.ls('/tmp')

print(ls)
