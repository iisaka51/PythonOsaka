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

p1 = Price(10)
p2 = Price(20)

print(p1 == p2)
print(p1 != p2)
print(p1 <  p2)
print(p1 <= p2)
print(p1 >  p2)
print(p1 >= p2)
