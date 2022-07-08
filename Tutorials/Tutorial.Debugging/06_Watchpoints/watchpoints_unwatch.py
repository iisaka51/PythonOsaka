from watchpoints import watch, unwatch

a = 0
watch(a)
a = 1           # trigger
unwatch(a)
a = 2           # nothing will happen
