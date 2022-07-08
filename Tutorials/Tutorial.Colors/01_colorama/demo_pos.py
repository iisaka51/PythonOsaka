from colorama import init, Cursor, ansi

pos = Cursor.POS

def main():
    init()
    print(ansi.clear_screen())
    print(pos(1,1) + "Hello")
    print(pos(1,2) + "Python")
    print(pos(1,3) + "Hello")
    print(pos(1,4) + "Python")

if __name__ == '__main__':
    main()
