from watchpoints import watch

class CB:
    def __init__(self):
        self.counter = 0

    def __call__(self, *args):
        self.counter += 1


cb = CB()
watch.config(callback=cb)
a = [1, 2, 3]
watch(a)
a[0] = 2
a.append(4)
b = a
b.append(5)
a = {"a": 1}
a["b"] = 2
