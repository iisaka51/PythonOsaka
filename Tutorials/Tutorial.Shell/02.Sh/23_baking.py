from sh import ls

# "/usr/bin/ls -la"
ls = ls.bake("-la")
print(ls)

# "ls -la /tmp"
print(ls("/tmp"))
