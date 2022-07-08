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

