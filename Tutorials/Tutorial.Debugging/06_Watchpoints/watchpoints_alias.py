from watchpoints import watch, unwatch

def myfunc():
    a = 0
    watch(a, alias="myfunc")
    a = 1

myfunc()

# 何かしらの処理...

unwatch("myfunc")
a = 3
