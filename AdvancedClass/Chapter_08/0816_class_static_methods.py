class Queen(object):
    def print_vocal():
        print("Freddie")

class Whitesnake(object):
    @staticmethod
    def print_vocal():
        print("David")

queen = Queen()
new_queen = Queen()
print(queen.print_vocal)
print(new_queen.print_vocal)
print(Queen.print_vocal)

whitesnake = Whitesnake()
new_whitesnake = Whitesnake()
print(whitesnake.print_vocal)
print(new_whitesnake.print_vocal)
print(Whitesnake.print_vocal)
