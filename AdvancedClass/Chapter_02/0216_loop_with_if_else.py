data = list()
for i in range(10):
    if i % 2 == 0:
        data.append(i)
    else:
        data.append(str(i))
print(data)
# Output: [0, '1', 2, '3', 4, '5', 6, '7', 8, '9']
