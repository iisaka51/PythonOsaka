def test_sum1():
    assert sum([1,2,3]) == 6, "Expecting 6"

def test_sum2():
    assert sum([0,1,2]) == 6, "Expecting 6"

def test_sum3():
    assert sum((1,2,3)) == 6, "Expecting 6"

if __name__ == '__main__':
    test_sum1()
    test_sum2()
    test_sum3()
    print('All testcase passed.')
