def add(x, y):
    return x + y

def multiply(x, y):
    return x * y

def square(n):
    return(n**2)

def cube(n):
    return(n**3)

def fibonacci(n):
    a, b = 1, 0
    for _ in range(n+1):
        a, b = b, a + b
    return b
