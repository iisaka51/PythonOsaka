import array

a = array.array('i', [1,2,3,4,5])
b = array.array('i', [6,7,8,9,10])
for i in range(5):
    print(a[i]+b[i])

print(a + b)
