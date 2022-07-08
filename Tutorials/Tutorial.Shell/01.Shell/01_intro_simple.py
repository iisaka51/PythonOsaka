from shell import shell

ls = shell('ls')
for file in ls.output():
    print(file)
