f = open('data.txt')
data = f.readlines()
f.close()
print(data[0])
print(data)

for line in data:
    print(line)
