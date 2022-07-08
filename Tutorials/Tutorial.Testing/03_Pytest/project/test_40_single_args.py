import pytest
import mymath

test_square_data = [
    ( 3,  9),
    ( 4, 16),
    ( 5, 25),
]

test_cube_data = [
    ( 3, 27),
    ( 4, 64),
    ( 5, 125),
]

class TestMymath_SingleArgs:

    @pytest.mark.square
    @pytest.mark.parametrize('n, expect', test_square_data)
    def test_square(self, n, expect):
        v = mymath.square(n)
        assert v == expect, f'Expecting {expect}'

    @pytest.mark.cube
    @pytest.mark.parametrize('n, expect', test_cube_data)
    def test_cube(self, n, expect):
        v = mymath.cube(n)
        assert v == expect, f'Expecting {expect}'
