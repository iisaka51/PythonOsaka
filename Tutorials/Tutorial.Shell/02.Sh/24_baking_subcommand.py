from sh import ssh

iam1 = ssh("myserver.com", "-l", "iisaka", "whoami")

myserver = ssh.bake("myserver.com", l='iisaka')
iam2 = myserver.whoami()
v1 = iam1 == iam2

# print(myserver)
# print(v1)
# print(iam2)
