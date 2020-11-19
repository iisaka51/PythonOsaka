class Price(object):
  def __init__(self, price=0):
      self.price = price

  def __eq__(self, other):
      if other is None or not isinstance(other, Price):
          return NotImplemented
      return self.price == other.price

  def __ne__(self, other):
      return not self.__eq__(other)

p1 = Price(10)
p2 = Price(20)

print(p1 == p1)
print(p1 != p2)
print(p1.__eq__(1))
print(p1 == 1)
