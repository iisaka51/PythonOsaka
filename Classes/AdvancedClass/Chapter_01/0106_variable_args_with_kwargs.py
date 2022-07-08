def mysum(*argn, arg1, arg2):
    sum = 0
    for n in argn:
        sum += n
    print('SUM:', sum)

mysum(3,arg1=1,arg2=2)
mysum(3,4,5,arg1=1,arg2=2)
mysum(arg1=1,arg2=2,3)
