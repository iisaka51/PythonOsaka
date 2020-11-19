a=[1,2,3,4,5,6,7,8,9]
b=[9,8,7,6,5,4,3,2,1]

def  func1():
    for x in a:
        for y in b:
            if x == y:
                 yield (x)
%timeit {c for c in func1()}
