import pytest

@pytest.mark.sum01
def test_group2_sum01():
    assert sum([1,2,3]) == 6, "Expecting 6"

@pytest.mark.sum02
def test_group2_sum02():
    assert sum([0,1,2]) == 6, "Expecting 6"

@pytest.mark.sum03
def test_group2_sum03():
    assert sum((1,2,3)) == 6, "Expecting 6"
