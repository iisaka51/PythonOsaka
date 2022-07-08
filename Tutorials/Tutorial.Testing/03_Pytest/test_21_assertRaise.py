import unittest
from fraction import Fraction

def sum(arg):
    total = 0
    for val in arg:
        total += val
    return total

class TestSum(unittest.TestCase):
    def test_list_int(self):
        """
        整数のリストを加算できるかどうかのテスト
        """
        data = [1, 2, 3]
        result = sum(data)
        self.assertEqual(result, 6)

    def test_list_fraction(self):
        """
        分数のリストをまとめることができることをテスト
        """
        data = [Fraction(1, 4), Fraction(1, 4), Fraction(2, 5)]
        result = sum(data)
        self.assertEqual(result, 1)

    def test_bad_type(self):
        """
        文字列を入力に与えたテスト
        """
        data = "banana"
        with self.assertRaises(TypeError):
            result = sum(data)

if __name__ == '__main__':
    unittest.main()
