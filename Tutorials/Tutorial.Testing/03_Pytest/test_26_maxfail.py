import pytest

def fibonacci(n):
    a, b = 1, 0
    for _ in range(n+1):
        a, b = b, a + b
    return b

test_data = [
    ( 8,  34),
    ( 9,  56),   # 正解: 55
    (10,  90),   # 正解: 89
    (11, 144),
]

@pytest.mark.parametrize("n, expect", test_data)
def test_fibonacci(n, expect):
    result = fibonacci(n)
    assert result == expect
