a=[1,2,3,4,5,6,7,8,9]
b=[9,8,7,6,5,4,3,2,1]

def func2():
    return set(a) & set(b)

#%timeit func2()
print(func2())
