def mysum(arg1, arg2, *argn):
    total = 0
    for n in argn:
        total += n
    print('SUM:', total)

mysum(1,2)
mysum(1,2,3)
mysum(1,2,3,4,5) # エラーになる
