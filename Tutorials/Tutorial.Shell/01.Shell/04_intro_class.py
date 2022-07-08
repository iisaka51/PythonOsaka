from shell import Shell

sh = Shell()
sh.run('ls /tmp')
for file in sh.output():
    print(file)

