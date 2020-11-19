class Price:
  def __init__(self, price=0):
      self.price = price

  def __eq__(self, other):
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


if __name__ == '__main__':
    p1 = Price(10)
    p2 = Price(20)

    print(f'p1 = {p1.price} , p2 = {p2.price}')
    print('p1 + p2 = ', p1 + p2)
    print('p2 + p1 = ', p2 + p1)
    print('p1 - p2 = ', p1 - p2)
    print('p2 - p1 = ', p2 - p1)
    print('p1 * p2 = ', p1 * p2)
    print('p2 * p1 = ', p2 * p1)
    print('p1 / p2 = ', p1 / p2)
    print('p2 / p1 = ', p2 / p1)
