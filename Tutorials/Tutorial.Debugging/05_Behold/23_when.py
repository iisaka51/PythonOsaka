from behold import Behold

for x in range(10):
    _ = Behold().when(x == 1).show('x')
