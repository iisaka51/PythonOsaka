from colorama import init, Cursor, ansi

up = Cursor.UP
down = Cursor.DOWN
forward = Cursor.FORWARD
back = Cursor.BACK

def main():
    init()
    print(ansi.clear_screen())
    print("Bonjour")
    print(up() + ansi.clear_line() + 'Hello')
    print("Bonjour")
    print(up() + 'Hello')
    print("Python")
    print("Osaka")
    print(up(2) + 'p' + down() + back() + 'o')

if __name__ == '__main__':
    main()
