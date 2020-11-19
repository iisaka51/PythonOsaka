def dispatcher(operator, x, y):
    dispatch_dict= {
        'add': lambda: x + y,
        'sub': lambda: x - y,
        'mul': lambda: x * y,
        'div': lambda: x / y,
    }
    return dispatch_dict.get(operator, None)()

print(dispatcher('mul', 3, 5))
print(dispatcher('abc', 3, 5))
exit(0)

def dispatcher(operator, x, y):
    return {
        'add': lambda: x + y,
        'sub': lambda: x - y,
        'mul': lambda: x * y,
        'div': lambda: x / y,
    }.get(operator, lambda: None)()

print(dispatcher('mul', 3, 5))
print(dispatcher('abc', 3, 5))

