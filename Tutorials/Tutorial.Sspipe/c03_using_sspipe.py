import os
from sspipe import p

( os.listdir(".")
    | p(filter, os.path.isfile)
    | p(map, lambda x: [x, os.path.getsize(x)])
    | p(sorted, key=lambda x: x[1], reverse=True)[:5]
    | p(dict)
    | p(print)
)
