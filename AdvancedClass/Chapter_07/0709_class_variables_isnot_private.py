class Point:
    points = 0
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.points += 1

p1 = Point()
print(p1.points)
p2 = Point()
print(p2.points)
