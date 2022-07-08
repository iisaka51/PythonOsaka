from shell import shell

ls = shell('ls /tmp')
for file in ls.output():
    print(file)
