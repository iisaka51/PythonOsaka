max_num = 400_0000
euler2 = 0

a, b = 0, 1
while(a <= max_num):
    a, b = b, a + b
    if b % 2 == 0:
        euler2 += b

# コードは短いけれど代入がループごとに発生するため遅くなる
#
# while(a <= max_num):
#     a, b, euler2 = b, a + b, (euler2 + a) if a % 2 == 0 else euler2
#

assert euler2 == 4613732
