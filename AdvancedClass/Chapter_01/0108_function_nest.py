def squre(number):
    def multiple_me(number):
        return number * number

    return multiple_me(number)

print(dir(squre))
print(squre(3))
