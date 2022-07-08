from watchpoints import watch

def func(var):
    var["a"] = 1

a = {}
watch(a)
func(a)
