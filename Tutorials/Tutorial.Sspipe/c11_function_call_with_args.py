X = "Hello "
print(X, "World",  end='!\n')

from sspipe import p
"Hello " | p(print, "World", end='!\n')
