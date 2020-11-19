# range(0,10,2) とすれば if はいらない。あくまで例示のため (^o^)
data = list()
for i in range(10):
    if i % 2 == 0:
        data.append(i)
print(data)
# Output: [0, 2, 4, 6, 8]
