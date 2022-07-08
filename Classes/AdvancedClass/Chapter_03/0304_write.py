f = open('data.txt')
data = f.read()
f.close()

f = open('new_data.txt', 'w')
f.write(data)
f.close()
