def squre(n):
    return(n**2)
def cube(n):
    return(n**3)

operations = [squre, cube]

data = [1, 2, 3, 5, 8, 11, 19]

# data の要素が偶数なら squre, 奇数なら cube を実行する
# 普通の方法
for v in data:
    if v%2 == 0:
        result = squre(v)
        print(f'squre({v}):', result)
    else:
        result = cube(v)
        print(f'cube({v}):', result)

# より洗練された方法
for v in data:
    n = v%2
    action = operations[n]
    print(f"{action.__name__}({n}):", action(v))
