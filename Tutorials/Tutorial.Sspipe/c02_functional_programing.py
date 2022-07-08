import os

print(dict(sorted(
    map(
        lambda x: [x, os.path.getsize(x)],
        filter(os.path.isfile, os.listdir("."))
    ), key=lambda x: x[1], reverses=True)
)[:5]))
