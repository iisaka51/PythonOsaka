from watchpoints import watch

a = []
watch(a)
a = {}      # Trigger
a["a"] = 2  # Trigger
