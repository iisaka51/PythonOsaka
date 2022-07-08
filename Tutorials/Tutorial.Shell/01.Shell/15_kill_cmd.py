from shell import Shell

sh = Shell(has_input=True)
v1 = sh.run('./Sleeper.sh')
v2 = sh.kill()

# v1.output()
# v2.output()
