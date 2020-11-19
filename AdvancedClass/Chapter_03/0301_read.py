f = open('data.txt')
data = f.read()
f.close()
print(type(data))
print(data)

lines = data.split('\n')
for line in lines:
    print(line)
