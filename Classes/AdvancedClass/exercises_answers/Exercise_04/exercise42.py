class Price:
  """
  This is help messages for CLASS: Price
  """
  def __init__(self, price=0):
      self.price = price

  def __eq__(self, other):
      """ EQUAL: Return self==value """
      if other is None or not isinstance(other, Price):
          return NotImplemented
      return self.price == other.price

  def __ne__(self, other):
      return not self.__eq__(other)

  def __lt__(self, other):
      if not isinstance(other, Price):
          return NotImplemented
      return self.price < other.price

  def __le__(self, other):
      return self.__lt__(other) or self.__eq__(other)

  def __gt__(self, other):
      return not self.__le__(other)

  def __ge__(self, object):
      return not self.__lt__(object)

  def __add__(self, other):
      if other is None or not isinstance(other, Price):
          return NotImplemented
      return self.price + other.price

  def __sub__(self, other):
      if other is None or not isinstance(other, Price):
          return NotImplemented
      return self.price - other.price

  def __mul__(self, other):
      if other is None or not isinstance(other, Price):
          return NotImplemented
      return self.price * other.price

  def __truediv__(self, other):
      if other is None or not isinstance(other, Price):
          return NotImplemented
      return self.price / other.price

  def __str__(self):
      return str(self.price)

if __name__ == '__main__':
    p1 = Price(10)
    p2 = Price(20)

    print(f'p1 = {p1} , p2 = {p2}')
    print('p1 + p2 = ', p1 + p2)
    print('p2 + p1 = ', p2 + p1)
    print('p1 - p2 = ', p1 - p2)
    print('p2 - p1 = ', p2 - p1)
    print('p1 * p2 = ', p1 * p2)
    print('p2 * p1 = ', p2 * p1)
    print('p1 / p2 = ', p1 / p2)
    print('p2 / p1 = ', p2 / p1)
