def test_group1_sum1():
    assert sum([1,2,3]) == 6, "Expecting 6"

def test_group1_sum2():
    assert sum([0,1,2]) == 6, "Expecting 6"

def test_group1_sum3():
    assert sum((1,2,3)) == 6, "Expecting 6"
