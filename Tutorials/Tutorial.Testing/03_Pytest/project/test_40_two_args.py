import pytest
import mymath

test_add_data = [
    (10, 20, 30),
    (15, 25, 40),
    (20, 30, 50),
]

test_multiply_data = [
    (10, 20, 200),
    (15, 25, 375),
    (20, 30, 600),
]

class TestMymath_TwoArgs:

    @pytest.mark.add
    @pytest.mark.parametrize('a, b, expect', test_add_data)
    def test_add(self, a, b, expect):
        v = mymath.add(a, b)
        assert v == expect, f'Expecting {expect}'

    @pytest.mark.multiply
    @pytest.mark.parametrize('a, b, expect', test_multiply_data)
    def test_multiply(self, a, b, expect):
        v = mymath.multiply(a, b)
        assert v == expect, f'Expecting {expect}'
