from watchpoints import watch

a = []
watch(a, track="object")
a.append(1)   # Trigger
a = {}        # オブジェクトが変わっていないので、何も起きない

a = []
watch(a, track="variable")
a.append(1)   #  'a' は同じオブジェクトなので、何も起きない
a = {}        # Trigger
