import unittest
from mymath import add, multiply, square, cube


class MyMathFixtureTest(unittest.TestCase):
    test_data = {
        'Add': {'a':10, 'b': 20, 'expect': 30},
        'Multiply': {'a':5,  'b': 6, 'expect': 30},
        'Square': {'a':5,  'b': None, 'expect': 25},
    }

    @classmethod
    def setUpClass(cls):
        print(f'\ncalled once before any tests in {cls.__name__}')

    @classmethod
    def tearDownClass(cls):
        print(f'\ncalled once after all tests in {cls.__name__}')


    def setUp(self):
        self.a = 0
        self.b = 0
        name = self.shortDescription()
        self.a = self.test_data[name]['a']
        self.b = self.test_data[name]['b']
        print(f'\nSetup for {name}: {self.a}, {self.b}')

    def tearDown(self):
        print(f'\nEnd of test {self.shortDescription()}')

    def testAdd(self):
        """Add"""
        result = add(self.a, self.b)
        self.assertTrue(result == self.test_data['Add']['expect'])

    def testMultiply(self):
        """Multiply"""
        result = multiply(self.a, self.b)
        self.assertTrue(result == self.test_data['Multiply']['expect'])

    def testSquare(self):
        """Square"""
        result = square(self.a)
        self.assertTrue(result == self.test_data['Square']['expect'])


if __name__ == '__main__':
    unittest.main()
