def add(x, y):
    """
    >>> add(10, 20)
    30
    """
    return x + y

def multiply(x, y):
    """
    >>> multiply(5, 6)
    30
    """
    return x * y

def square(n):
    """
    >>> square(5)
    25
    """
    return(n**2)

def cube(n):
    """
    >>> cube(5)
    125
    """
    return(n**3)

def fibonacci(n):
    """
    >>> mymath.fibonacci(10)
    89
    """
    a, b = 1, 0
    for _ in range(n+1):
        a, b = b, a + b
    return b
