import pytest

@pytest.mark.parametrize('a', [5, 10])
@pytest.mark.parametrize('b', [6, 12])
@pytest.mark.parametrize('c', [7, 14])
def test_sum(a, b, c):
    pass
