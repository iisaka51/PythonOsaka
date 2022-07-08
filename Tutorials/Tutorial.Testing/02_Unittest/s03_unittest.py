import unittest


class TestSum(unittest.TestCase):

    def test_sum1(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Expecting 6")

    def test_sum2(self):
        self.assertEqual(sum([0, 1, 2]), 6, "Expecting 6")

    def test_sum3(self):
        self.assertEqual(sum((1, 2, 3)), 6, "Expecting 6")

if __name__ == '__main__':
    unittest.main()
