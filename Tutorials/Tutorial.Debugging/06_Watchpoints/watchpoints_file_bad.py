from watchpoints import watch

a = 0
with open("watch.log", "w") as f:
    watch(a, file=f)
a = 1
