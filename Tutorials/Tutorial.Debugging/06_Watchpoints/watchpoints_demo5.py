from watchpoints import watch

class MyObj:
    def __init__(self):
        self.a = 0

obj = MyObj()
d = {"a": 0}
watch(obj.a, d["a"])  # こんなこともできる
obj.a = 1             # Trigger
d["a"] = 1            # Trigger
