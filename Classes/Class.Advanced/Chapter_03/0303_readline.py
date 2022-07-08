f = open('data.txt')
line = f.readline()
print(type(line))

while line:
    print(line)
    line = f.readline()

f.close()
