from watchpoints import watch

with open("watch.log", "w") as f:
    a = 0
    watch(a, file=f)
    a = 1
