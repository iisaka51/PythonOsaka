def mysquare():
    i = 1;

    while True:
        yield i*i
        i += 1

for num in mysquare():
    if num > 30:
         break
    print(num)
