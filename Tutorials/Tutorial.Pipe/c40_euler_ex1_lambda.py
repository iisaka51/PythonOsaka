max_num = 1000
mul_3_5 = [i for i in range(1,max_num) if i % 3 == 0 or i % 5 == 0]
euler1 = sum(mul_3_5)
assert euler1 == 233168
