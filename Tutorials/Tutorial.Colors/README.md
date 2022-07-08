コンソールに文字をカラー出力してみよう
=================
## はじめに
Pythonでコンソールに文字を出力するときに色を制御する方法には、いくつかあります。

- 直接 ANSIエスケープコードを指定する
- colarama を利用する
- termcolor を利用する
- string-color を利用する

colorama と termcolor、string-color  も内部的には ANSIエスケープコードを出力して制御しています。ANSI規格ですが、実際に期待通りに出力できるかは、ターミナルのエミュレートソフトに依存しています。

 ターミナル別のスタイル対応

| Terminal | bold | dark | underline | blink | reverse | concealed |
|:--|:--|:--|:--|:--|:--|:--|
| xterm | yes | no | yes | bold | yes | yes |
| linux | yes | yes | bold | yes | yes | no |
| rxvt | yes | no | yes | bold/black | yes | no |
| dtterm | yes | yes | yes | reverse | yes | yes |
| teraterm | reverse | no | yes | rev/red | yes | no |
| aixterm | normal | no | yes | no | yes | yes |
| PuTTY | color | no | yes | no | yes | no |
| Windows | no | no | no | no | yes | no |
| Cygwin SSH | yes | no | color | color | color | yes |
| Mac Terminal | yes | no | yes | yes | yes | yes |


## colorama について
[colorama ](https://pypi.org/project/colorama/) はANSI エスケープ文字シーケンスを使って、色付きの端末テキストやカーソル位置を制御することができるPython の拡張モジュールです。Windows 上でも期待どおりに動作させることができます。逆にいうとWindowsでできることに合わせているとも言えます。


### インストール
colorama はコンソール出力を行うライブラリやパッケージで広く使われているため、いつの間にかインストールされているかもしれません。個別にインストールする場合は、 pip コマンドを使います。

 bash
```
 $ pip install colorama
```


### colorama の使用方法
colorama で前景色(Foregroud Color)、背景色(Background Color)、スタイル(Style) を制御するためのクラスが提供されています。


 color.py
```
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
     
```

はじめに呼び出している  `init()` はプラットフォームが Windows のときは必須ですが、Linux などでは不要なものです。しかし、呼び出しても問題になならないようになっているため、コードの汎用性のために呼び出すようにします。

メッセージをカラー表示させるために定義した `cprint()` では、内部で `print()` を呼び出して、
BRIGHTNESS と COLOR の設定、それをリセットをメッセージの前後に出力しているだけです。

 `Style` には  `DIM` は Dimensiton Style のことで、  `NORMAL` は歴史的な理由から区別されていますが、実際には同じものです。


 demo.py
```
 
 from color import *
 
 for fore in FORES:
     for brightness in BRIGHTNESS:
         cprint("Python Osaka", color=fore, brightness=brightness)
 
```

これを実行すると次のような出力になります。

![](https://gyazo.com/7f84a3002ceb5c476fadf4ab6c96e265.png)
最初の部分が欠けて見えるのは、背景色と前景色が同じ黒（BLACK)であるためです。

 demo_with_background.py
```
 from color import *
 
 for fore in FORES:
     for back in BACKS:
         for brightness in BRIGHTNESS:
             cprint("Python", color=back+fore, brightness=brightness, end=' ')
             
```

![](https://gyazo.com/7bd16ebd35a32a609dc594466a7fa37a.png)

### 標準エラー出力
標準エラー出力へ出力する場合は次のようになります。

 demo_srderr.py
```
 from color import *
 import sys
 
 print(Fore.GREEN + 'GREEN set on stdout. ', end='')
 print(Fore.RED + 'RED redirected stderr', file=sys.stderr)
 print(
 ('Further stdout should be GREEN, '
  'i.e., the stderr redirection should not affect stdout.'))
  
```

この場合、標準エラー出力には赤(RED)で出力されます。
つぎのように標準エラー出力をリダイレクトした場合は通常どおりとなります。

 bash
```
 $ python demo_stderr.py 2>error.txt
```

![](https://gyazo.com/9b9225905175764f5095376e46975cf5.png)

## colorama_test()
これまでの方法では、 `init()` と  `print(Style.RESET_ALL)` を明示的に記述する必要があります。 `colarama_text()` はこれを自動的に処理してくれるコンテキストマネージャーです。

 colorama_text.py
```
 from colorama import colorama_text, Fore
 
 def main():
     """automatically reset stdout"""
     with colorama_text():
         print(Fore.GREEN + 'text is green')
         print(Fore.RESET + 'text is back to normal')
 
     print('text is back to stdout')
 
 if __name__ == '__main__':
     main()
```

### カーソル移動
colorama ではカーソルの移動もサポートしています。

-  `UP()` - カーソルを1行上に移動
-  `DOWN()` - カーソルを1行下に移動
-  `FORWARD()` - カーソルを1文字右に移動
-  `BACK()` - カーソルを1文字左に移動
-  `POS(x, y)` - 指定したターミナル座標(x, y)にカーソルを移動

 `colorama.ansi` ではつぎのユーティリティー関数が提供されています。

-  `clear_screen()` - ターミナルをクリア
-  `clear_line()` ターミナルでカーソルがある行をクリア

 demo_cursor.py
```
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
```

 demo_pos.py
```
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
```

colorama モジュールを使うと簡単にクロスプラットフォームなカラー制御を行うことができるようになります。

## termcolor について
termcolor は ANSIエスケープコードを簡単に処理してくれるPython モジュールで、コンソールへテキストを色指定して出力することができます。スタイルは指定することができても、実際に表示できるかどうかはターミナルソフトに依存しているため、期待通りに出力できないこともあることに注意してください。


### インストール
terncolor は pip コマンドでインストールすることができます。

 bash
```
 $ pip install termcolor
```

### termcolor の使用方法

termcolor の使用方法は次のようになります。

 color.py
```
 from termcolor import cprint, colored
 
 # 指定可能な前景色
 FORES = [ 'grey', 'red', 'green', 'yellow',
           'blue', 'magenta', 'cyan', 'white' ]
 
 # 指定可能な背景色
 BACKS = [ 'on_grey', 'on_red', 'on_green', 'on_yellow',
           'on_blue', 'on_magenta', 'on_cyan', 'on_white' ]
 
 # 指定可能なスタイル
 STYLES = [ 'bold', 'dark', 'underline', 'blink', 'reverse', 'concealed' ]
 
```

 `cprint(text, color=None, on_color=None, attrs=None, **kwargs)` 
-  `color` : 前景色を文字列で与える
-  `on_color` ：背景色を文字列で与える
-  `attrs` スタイルを文字列で与える

 demo.py
```
 from color import *
 
 for fore in FORES:
     for back in BACKS:
         for style in STYLES:
             cprint("Python", color=fore, on_color=back,
                              attrs=[style], end=' ')
                              
```

![](https://gyazo.com/edb31109d8511fa33e57b31e650e2cf8.png)

 `cprint()` は  `colored()` で処理したテキストを `print()` としているだけです。

 demo_text.py
```
 from color import *
 
 text = colored("Python Osaka", color='yellow', on_color='on_red')
 print(text)
 
```

### 環境変数 ANSI_COLORS_DISABLED
環境変数  `ANSI_COLORS_DISABLED` が何か設定されているとカラー制御は無視されます。

 bash
```
 $ env ANSI_COLORS_DISABLED=1 python demo_text.py
```

![](https://gyazo.com/dc23c75309b0cdc7f9facd602cc740ca.png)


### Windowsでの利用
termcolor 単独では WIndows で期待通りには動作しません。Windowsでは、 `colorama.init()` を呼び出せばOKです。

 demo_windows.py
```
 mport colorma
 from color import *
 
 colorma.init()
 text = colored("Python Osaka", color='yellow', on_color='on_red')
 print(text)
 
```

はじめから colorama を使えばよいのでは？　と思うかもしれません。termcolor はサポートしているANSIエスケープコードが多いことから用途に応じて使いわけることになるでしょう。

## string-color について
string-color は RGBコードを指定することで256色をサポートしているのが特徴です。内部的には colorama を利用しているので Windows でも期待通りに出力させることができます。

### インストール
stting-color は pip コマンドでインストールすることができます。

 bash
```
 $ pip iinstall string-color
```

### string-color の利用方法
string-color にはいくつかのコマンドラインツール string-color も提供されます。

 bash
```
 $ string-color --help
 usage: string-color [-h] [-x] [-r] [--hsl] [-a] [-v] [color]
 
 just another mod for printing strings in color.
 
 positional arguments:
   color          show info for a specific color:
                  $ string-color red
                  $ string-color '#ffff87'
                  $ string-color *grey* # wildcards acceptable
                  $ string-color '#E16A7F' # any hex not found will return the closest match
 
 options:
   -h, --help     show this help message and exit
   -x, --hex      show hex values
   -r, --rgb      show rgb values
   --hsl          show hsl values
   -a, --alpha    sort by name
   -v, --version  show program's version number and exit
   
```

引数なしで実行すると256色のカラーを表示します。

![](https://gyazo.com/996e44d475eac7377578209945758eed.png)
色名、RGBコードを引数に与えるとその色の情報を表示します。

 bash
```
 $ string-color red
  Red #ff0000 rgb(255,0,0) hsl(0,100%,50%)
```

![](https://gyazo.com/4f79808e86918d27c940767b84fc5067.png)
 bash
```
 string-color '#ffff87'
  Khaki #ffff87 rgb(255,255,135) hsl(60,100%,76%)
```

![](https://gyazo.com/f73871469e0f916342a7480f25a3828d.png)
 bash
```
 $ string-color '*grey*'
  DarkGrey #3a3a3a rgb(58,58,58) hsl(0,0%,22%)
  DarkGrey2 #303030 rgb(48,48,48) hsl(0,0%,18%)
  DarkGrey3 #262626 rgb(38,38,38) hsl(0,0%,14%)
  DarkGrey4 #1c1c1c rgb(28,28,28) hsl(0,0%,10%)
  DarkGrey5 #121212 rgb(18,18,18) hsl(0,0%,7%)
  DarkGrey6 #080808 rgb(8,8,8) hsl(0,0%,3%)
  Grey #808080 rgb(128,128,128) hsl(0,0%,50%)
  Grey2 #808080 rgb(128,128,128) hsl(0,0%,50%)
  Grey3 #767676 rgb(118,118,118) hsl(0,0%,46%)
  Grey4 #6c6c6c rgb(108,108,108) hsl(0,0%,40%)
  Grey5 #626262 rgb(98,98,98) hsl(0,0%,37%)
  Grey6 #5f5f5f rgb(95,95,95) hsl(0,0%,37%)
  Grey7 #585858 rgb(88,88,88) hsl(0,0%,34%)
  Grey8 #4e4e4e rgb(78,78,78) hsl(0,0%,30%)
  Grey9 #444444 rgb(68,68,68) hsl(0,0%,26%)
  LightGrey #eeeeee rgb(238,238,238) hsl(0,0%,93%)
  LightGrey10 #a8a8a8 rgb(168,168,168) hsl(0,0%,65%)
  LightGrey11 #9e9e9e rgb(158,158,158) hsl(0,0%,61%)
  LightGrey12 #949494 rgb(148,148,148) hsl(0,0%,58%)
  LightGrey13 #8a8a8a rgb(138,138,138) hsl(0,0%,54%)
  LightGrey14 #878787 rgb(135,135,135) hsl(0,0%,52%)
  LightGrey2 #e4e4e4 rgb(228,228,228) hsl(0,0%,89%)
  LightGrey3 #dadada rgb(218,218,218) hsl(0,0%,85%)
  LightGrey4 #d7d7d7 rgb(215,215,215) hsl(0,0%,84%)
  LightGrey5 #d0d0d0 rgb(208,208,208) hsl(0,0%,81%)
  LightGrey6 #c6c6c6 rgb(198,198,198) hsl(0,0%,77%)
  LightGrey7 #bcbcbc rgb(188,188,188) hsl(0,0%,73%)
  LightGrey8 #afafaf rgb(175,175,175) hsl(0,0%,68%)
  LightGrey9 #b2b2b2 rgb(178,178,178) hsl(0,0%,69%)
  LightSlateGrey #8787af rgb(135,135,175) hsl(240,20%,60%)
```

![](https://gyazo.com/e6a2ffcae9d95e779b572dcc51a79f8b.png)

### プログラム
string-color は次のユーティリティー関数を提供しています。

-  `cs()` - 与えたテキストに色やスタイルを適用させたANSIエスケープコードを生成します。これを `print()` で出力することで、コンソールにテキストをカラー表示させることができます。
-  `bold()` - 与えたテキストをアンダーライン表示させる
-  `bold()` - 与えたテキストをボールド表示させる

 demo.py
```
 from stringcolor import *
 
 # a few examples without background colors.
 # for color names see CLI usage below.
 print(cs("here we go", "orchid"))
 print(cs("away to space!", "DeepPink3"))
 print(cs("final fantasy", "#ffff87"))
 print()
 
 # bold and underline also available.
 print(cs("purple number 4, bold", "purple4").bold())
 print(cs("blue, underlined", "blue").underline())
 print(bold("bold AND underlined!").underline().cs("red", "gold"))
 print(underline("the bottom line."))
 print()
 
 # yellow text with a red background.
 # color names, hex values, and ansi numbers will work.
 print(cs("warning!", "yellow", "#ff0000"))
 print()
 
 # concat
 print(cs("wild", "pink")+" stuff")
 print("nothing "+cs("something", "DarkViolet2", "lightgrey6"))
 print()
 
 # use any working rgb or hex values.
 # it will find the closest color available.
 print(cs("this will show up red", "#ff0009"))
 print(cs("so will this", "rgb(254, 0, 1)"))
 print()
 
 # use with format and f-strings
 print(f"this is a test {cs('to check formatting with f-strings', 'yellow', 'grey').bold().underline()}")
 print("this is a test {}".format(cs('to check the format function', 'purple', 'lightgrey11').bold().underline()))
 
```

![](https://gyazo.com/cf98a154af8949a87dc0522d647fb8f6.png)
## まとめ


## 参考資料

- Colorama [ソースコード ](https://github.com/tartley/Colorama)
- termcolor [PyPI - termcolor ](https://pypi.org/project/termcolor/)
- string-color [PyPI string-color ](https://pypi.org/project/string-color/)
- Wikipedia - [ANSI Escape code ](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [ANSIエスケープコード ](https://www.mm2d.net/main/prog/c/console-02.html)
- [Build your own Command Line with ANSI escape codes ](https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html)
- [Ascii Table ](https://theasciicode.com.ar/) 
- [Web セーフカラー ](https://www.colordic.org/s)


