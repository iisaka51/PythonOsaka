import os

data = os.listdir(".")
data = filter(os.path.isfile, data)
data = map(lambda x: [x, os.path.getsize(x)], data)
data = dict(data)
print(data)
