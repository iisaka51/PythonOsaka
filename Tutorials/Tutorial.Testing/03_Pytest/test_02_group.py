class TestClass:

   def test_one(self):
      x = "Hello"
      assert 'H' in x

   def test_two(self):
      x = "Python"
      assert hasattr(x, 'size')
