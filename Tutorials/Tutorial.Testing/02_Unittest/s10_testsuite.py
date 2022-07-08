import unittest

from s06_class_fixture import MyMathFixtureTest


def suite():
   suite = unittest.TestSuite()
   suite.addTest(unittest.makeSuite(MyMathFixtureTest))
   suite.addTest(MyMathFixtureTest('testMultiply'))
   suite.addTest(MyMathFixtureTest('testSquare'))
   suite.addTest(MyMathFixtureTest('testAdd'))
   return suite

if __name__ == '__main__':
   runner = unittest.TextTestRunner()
   test_suite = suite()
   runner.run(test_suite)

