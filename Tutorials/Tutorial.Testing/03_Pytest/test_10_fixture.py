import pytest
@pytest.fixture
def input_value1():
        return [1, 2, 3]

@pytest.fixture
def input_value2():
        return [0, 1, 2]

@pytest.fixture
def input_value3():
        return (1, 2, 3)

def test_demo_sum1(input_value1):
    assert sum(input_value1) == 6, "Expecting 6"

def test_demo_sum2(input_value2):
    assert sum(input_value2) == 6, "Expecting 6"

def test_demo_sum3(input_value3):
    assert sum(input_value3) == 6, "Expecting 6"

