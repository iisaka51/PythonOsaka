X = "World"
print("Hello", X, end="!\n")

from sspipe import p, px
"World" | p(print, "World", px, end="!\n")
