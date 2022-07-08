from watchpoints import watch

a = []
watch(a)
a.append(1)    # Trigger
a = {}         # Trigger
