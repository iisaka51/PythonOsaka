import unittest
from s06_class_fixture import MyMathFixtureTest


testList = [MyMathFixtureTest,]
testLoad = unittest.TestLoader()

TestList = []
for testCase in testList:
   testSuite = testLoad.loadTestsFromTestCase(testCase)
   TestList.append(testSuite)

newSuite = unittest.TestSuite(TestList)
runner = unittest.TextTestRunner()
runner.run(newSuite)

