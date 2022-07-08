from watchpoints import watch

a = 0
watch(a, when=lambda x: x > 0)
a = -1    # nothing will happen
a = 1     # Trigger
