from colorama import init, Fore, Back, Style

init()      # Windows では必須

# 指定可能な前景色
FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW,
          Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]

# 指定可能な背景色
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW,
          Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]

# 指定可能なスタイル
BRIGHTNESS = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]

def cprint(msg, color=Fore.WHITE, brightness=Style.NORMAL, **kwargs):
    print(f"{brightness}{color}{msg}{Style.RESET_ALL}", **kwargs)
