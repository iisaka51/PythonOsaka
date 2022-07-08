TUIアプリケーションフレームワーク Rich を使ってみよう
=================
## Rich について

[rich ](https://github.com/willmcgugan/rich) は Python で実装されたTUIアプリケーションを作成するためのフレームワークです。
Jupyter notebook などからも使用することができます。

![](https://gyazo.com/247620979a1badc6b40facf52ddf0fd0.png)


### インストール
拡張モジュールなのでインストールが必要です。

 zsh
```
 % pip install rich
```


## デバッグツールとしての利用
本来はTUIアプリケーションのためのフレームワークなのですが、単にデバッグのためのツールとしても十分魅力的な機能を提供しています。

### print()関数
Python の組み込み関数 `print()` の代替となるもので、アトリビュートを整形して出力してくれます。

```
 >>> print("Hello World!", locals())
 Hello World! {'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>}
```


```
 from rich import print as rpint
 rprint("Hello World!", locals())
```

![](https://gyazo.com/524b17c99966ff266f381d04f5e0af13.png)

 `rich.print()` 関数はJupyter notebook や IPython でも機能します。

### pretty()関数
Python の REPL に適用すると、REPLでPythonデータ構造と構文が強調表示されて、自動的に整形されて出力されるようになります。


```
 >>> from rich import pretty
 >>> pretty.install()
```

![](https://gyazo.com/79584a3da39d5c438b38b673840d9616.png)

IPython では、入力時には Pythonデータ構造と構文が強調表示されますが、出力はそのままです。

### inspec()関数
Richには、任意のPythonオブジェクトの美しいレポートを生成をする  `inspect()` 関数があります。 

![](https://gyazo.com/0f6a6f721dba99f5156c6f10e1515e95.png)

## Consoleクラス
Rich は端末を制御するための `Console` クラスを提供しています。 


```
 from rich.console import Console
 console = Console()
```

 `Console` クラスのインスタンスを作成してから、この  `console` オブジェクトに対して操作をすることになります。

 `Console` クラスは、レンダリング時に次のプロパティを自動検出します。

-  `size` ：端末の現在のサイズ
-  `encoding` ：デフォルトのエンコーディング（通常は `utf-8` ）
-  `is_terminal` ： `True` なら `Console` インスタンスが端末にアクセスしている
-  `color_system` ：コンソールカラーシステムを含む文字列

### color_system
端末に色を書き込むためのいくつかの「標準」がありますが、すべてがサポートされているわけではありません。 Richは適切なカラーシステムを自動検出します。
 `color_system` の値を `Console` コンストラクターに指定して設定することもできます。

color_systemは、次のいずれかの値に設定することができます。

-  `None` ：色を完全に無効にする
-  `auto` ：カラーシステムを自動検出する
-  `standard` ：ノーマル(normal)８色、ブライト(bright)8色、合計16色が設定できる
-  `256` ： `standard` の16色と240色の固定パレットを設定できる
-  `truecolor` ：1670万色を設定できる
  - プラットフォームおよびモニターに依存しています
　 `windows` ：Windowsプラットフォームのターミナル
　	レガシーなWindowsターミナルでは8色を設定できる
　	新しいWindowsターミナルでは、 `truecolor` と同じ

### print()メソッド
 `Console.print()` メソッドは、 `rich.print()` 関数と同様の機能を提供します。


```
 from rich.console import Console
 console = Console()
 
 console.print([1, 2, 3])
 console.print("[blue underline]Looks like a link")
 console.print(locals())
 console.print("FOO", style="white on blue")
```

![](https://gyazo.com/46dd35c6b2057be4856138542f7c263c.png)

### log()メソッド
 `Console.log()` メソッドは、 `print()` メソッドと同じ機能を提供しますが、実行中のアプリケーションのデバッグに役立ついくつかの機能が追加されています。

![](https://gyazo.com/084b402e0ae9a2957d05fcf5317b56c5.png)

ログ出力の時間が出力とともに表示されます。
 `log()` メソッドに `log_locals=True` を与えると、Richは  `log()` が呼び出されたローカル変数を整形して表示するので、デバッグを手助けとなります。

![](https://gyazo.com/c967147f60ce64056efada3bfb21c12b.png)

### out()メソッド
 `Console` クラスには　 `print()` と `log()` の他にも  `out()` メソッドがあります。
これは、端末へ低レベルの出力を行います。
 `out()` メソッドは、与えられたすべての引数のオブジェクトを文字列に変換し出力します。整形することはしませんが、基本的なスタイルは適用することができ、オプションで強調表示を行います。

![](https://gyazo.com/013a1680f0983068a1450e0e8e84b9c8.png)

### rule()メソッド
 `Console.rule()` メソッドを使うと、横にラインを表示してくれます。
 `log()` メソッドと組み合わせて使うことでログメッセージが読みやすくなるものです。

![](https://gyazo.com/0480ce2da7f6fbb2e60cc30d1dfdc724.png)

### status()メソッド 

 `Console.status()` メソッドは、通常のコンソール出力に干渉しないスピナー・アニメーションと共にステータスメッセージを表示させることができます。
この機能のデモを行うには、次のコマンドを実行します。

 zsh
```
 % python -m rich.status
```

ステータスメッセージを表示するには、 `status()` にメッセージを与えて呼び出します。 
メッセージには、文字列、テキスト、またはその他のレンダリング可能オブジェクトを与えることができます。


```
 from rich.console import Console
 from time import sleep
 
 console = Console()
 
 with console.status("Do somethings..."):
     sleep(30)
```

 `console.status()` に キーワード引数 `spinner` にアニメーションのスタイルを与えて、アニメーションを変更することができます。また、 `spinner.speed` でアニメーション速度を変更することができます。

 `spinner` に与えることができるスタイルの一覧は、次のコマンドでデモとして確認できます。
 zsh
```
 % python -m rich.spinner
```

![](https://gyazo.com/e46208aac72451c1f7a8fb9cbdf9d147.png)

### テキストの整列と両揃え

 `console.print()` と  `console.log()` はどちらも、キーワード引数 `justify` を受付ます。
これには、 `default` 、 `left` 、 `right` 、 `center` 、 `full` のいずれかを設定します。

-  `left` ：テキストは端末の左に揃えに配置されて出力される
-  `right` ：テキストは端末の右に揃えに配置されて出力される
-  `center` ：テキストは端末の中央に配置され出力される
-  `full` ：テキストが中央揃えになります。 端末の左端と右端の両方に揃える
  - 英文の文章でよく見かけるスタイル

 `justify` のデフォルトは `default` で、 `left` と同じように見えますが、
微妙な違いがあります。
 `left` では端末の左に揃えて、テキストの右側にスペースが埋め込まれて両端に揃えられますが、 `default` ではスペースは埋め込まれません。
キーワード引数  `style` に背景色を設定するとこの違いを理解できるでしょう。


```
 rom rich.console import Console
 
 console = Console(width=20)
 
 style = "bold white on blue"
 console.print("default", style=style)
 console.print("left", style=style, justify="left")
 console.print("center", style=style, justify="center")
 console.print("right", style=style, justify="right")
```

![](https://gyazo.com/e265f5fa8549d9108e7227c41fb2f60c.png)

### Overflow
 `Console.print()` メソッドは、キーワード引数  `overflow` を与えて、出力しようとしているテキストが指定した文字幅を超えたときの制御を行うことができます。


```
 from typing import List
 from rich.console import Console, OverflowMethod
 
 console = Console(width=14)
 supercali = "Beautiful_is_better_than_ugly."
 
 overflow_methods: List[OverflowMethod] = ["fold", "crop", "ellipsis"]
 for overflow in overflow_methods:
     console.rule(overflow)
     console.print(supercali, overflow=overflow, style="bold blue")
     console.print()
```

![](https://gyazo.com/d9a25c9acd00655304fd7ee058e49190.png)

### input()
 `Console` クラスには、Pythonの組み込み関数  `input()` と同じように機能する、 `input()` メソッドがあります。プロンプトには、Richが出力できるものなら何でも使用することができます。 


```
 from rich.console import Console
 
 console = Console()
 console.input("What is [i]your[/i] [bold red]name[/]? :smiley: ")
```

![](https://gyazo.com/9b12e60611a689ad8376d7dcc1b8662e.png)


### エクスポート
 `Console` クラスは、書き込まれたものをテキストまたは HTML としてエクスポートすることができます。 エクスポートを有効にするためには、はじめにコンストラクターで  `record=True` を与えてインスタンスオブジェクトを生成しておきます。これにより、 `print()` や  `log()` メソッドで出力されるデータのコピーを保存するようになります。
出力したあとで、 `export_text()` や  `export_html()` を呼び出すことで、保存されているテキストを取り出し、 `save_texxt()` 、 `save_html()` メソッドを呼び出してファイルに保存することができます。
ただし、1度 `export_text()` や  `export_html()` を呼び出すと、保存されているテキストはクリアされてなくなることに注意してください。

 pytohn
```
 from rich.console import Console
 
 console = Console(record=True)
 console.print("Hello World!", style="white on blue")
 text1 = console.export_text()
 text2 = console.export_text()
 
 print(f'1st: {text1}')
 print(f'2nd: {text2}')
```


![](https://gyazo.com/9802ee234ad42393cb4ff2e0a9fedf1c.png)


```
 from rich.console import Console
 
 console = Console(record=True)
 console.print("Hello World!", style="white on blue")
 console.save_text(path='output.txt')
 
 console.print("Hello World!", style="white on blue")
 console.save_html(path='output.html')
```

 zsh
```
 % cat output.txt
 Hello World!
 
 % cat output.html
 <!DOCTYPE html>
 <head>
 <meta charset="UTF-8">
 <style>
 .r1 {color: #c0c0c0; background-color: #000080}
 body {
     color: #000000;
     background-color: #ffffff;
 }
 </style>
 </head>
 <html>
 <body>
     <code>
         <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span class="r1">Hello World!</span>
 </pre>
     </code>
 </body>
 </html>
```

### ファイルへの出力
 `Console` オブジェクトは標準出力（つまり端末）に出力します。はじめにコンストラクターでキーワード引数 `file` を設定することで、ファイルに出力するように指示することができます。
例えば、標準エラー出力へ出力したい場合は、次のようになります。


```
 import sys
 from rich.console import Console
 error_console = Console(file=sys.stderr)
 error_console.print("[bold red]This is an error!")
```

ここで、 `file` にはファイル名ではなく、これは、テキストを書き込むためにファイルオブジェクトである必要があります。 

```
 import sys
 from rich.console import Console
 
 with open('outout.txt', 'w') as fh:
     error_console = Console(file=fh)
     error_console.print("[bold red]This is an error!")
```

### 端末の内容を取り込む
端末に直接書き込むのではなく、 `Console` クラスからの出力をキャプチャしたい場合があります。 これは、コンテキストマネージャーを返す `Console.capture()` メソッドを使用して行うことができます。コンテキストマネージャーのブロックでは、 `print()` や  `og()` などの使用方法は変わらず、端末に出力したかのように処理されます。
このコンテキストマネージャーを終了してから、 `Console.get()` メソッドを呼び出して、端末に書き込まれたはずの文字列を取得します。


```
 from rich.console import Console
 
 console = Console()
 with console.capture() as capture:
     console.print("[bold red]Hello[/] World")
 output = capture.get()
```

### ページング

出力したいテキストが端末の行数を超えるような長い出力になるような場合、ページャーを使用して表示することができます。 ページャーは通常、オペレーティングシステムによるアプリケーションで、何かキーを押下してスクロールします。多くの場合、テキストやその他の機能を上下にスクロールすることをサポートするページャーもあります。

コンテキストマネージャーを返す  `Console.pager()` を呼び出すことにより、コンソールから出力をページングできます。 コンテキストブロックが終了すると、 `print()` などで出力した内容がオペレーティング・システムのぺージャーに渡されます。


```
 from rich.__main__ import make_test_card
 from rich.console import Console
 
 console = Console()
 with console.pager():
     console.print(make_test_card())
```

ほとんどのプラットフォームのデフォルトのページャーはカラー出力をサポートしていないため、Richは出力からカラーシーケンスを取り除きます。 ページャーがカラー出力ををサポートしていることがわかっている場合は、 `pager()` メソッドを呼び出すときに `styles=True` を設定することができます。

Linux系プラットフォームでは次のようにすると、ページャーとして `less` コマンドが起動されて、色付けのエスケープシーケンスは正しく処理することができます。

 zsh
```
 % export PAGER="less -R"
```

### 端末出力の自動検出
Rich は出力が端末ではないことを検出すると、出力から制御コードを取り除きます。 パイプを使って他のアプリケーションに出力を渡すような場合に便利です
制御コードもファイルに書き込みたい場合は、 `Console` クラスのコンストラクターで  `force_terminal=True` を設定します。

### 環境変数
Rich は次の環境変数の設定内容に従って動作します。

-  `TERM` ：端末の種別を表します。
  - これが  `dumb` もしくは  `unknown` に設定されていると、色とスタイル、およびプログレスバーなどのカーソルの移動が必要な一部の機能が無効になります。
-  `NO_COLOR` ：この環境変数が設定されている場合、Richは出力のすべての色を無効にします。

## スタイル
Rich では、テキストの色と太字、斜体などのさまざまな属性を定義するキーワード引数 `style` を設定することができます。 `style` にはスタイル定義を含む文字列や、 `Style` クラスのインスタンスオブジェクトを与えることができます。

### スタイルの定義
スタイル定義は、色と属性を設定するための1つ以上の単語を含む文字列です。

前景色を指定するには、[256の標準色 ](https://rich.readthedocs.io/en/latest/appendix/colors.html#appendix-colors) のいずれかを使用します。 たとえば、文字列 "Hello"を赤色で出力するためには、次のような方法があります。

```
 rom rich.console import Console
 
 console = Console()
 console.print("Hello", style="red")
 
 console.print("Hello", style="color(1)")
 
 console.print("Hello", style="#ff0000")
 console.print("Hello", style="rgb(255,0,0)")
```

色単独では前景色への指定になります。背景色を指定する場合は、その色の前に  `on` という単語を付けます。 次のコードは、白い背景に赤でテキストを印刷する例です。

 pytbon
```
 from rich.console import Console
 
 console = Console()
 console.print("DANGER!", style="red on white")
```

色指定では `default` も使用できます。この場合、端末ソフトウェアによって管理されるデフォルトの色が使用されます。 これは背景でも機能するので、  `style="default on default"` が端末のデフォルトのスタイルです。
他にも次のようなキーワードを指示することができます。

　 `bold` /  `b` ：テキストをボールド体で表示
-  `blink` ：テキストを点滅表示（使用するときは慎重に）
-  `blink2` ：テキストを点滅表示（点滅速度が速い）、サポートされている端末はほとんどない。
-  `conceal` ： テキストの隠蔽。サポートされている端末はほとんどない。
-  `italic` /  `i` ：テキストをイタリック体で表示。Windows端末ではサポートされていない。
-  `reverse` /  `r` ： テキストの前景色と背景色を入れ替えて表示する。
-  `strike` /  `s` ：テキストに打ち消し線をつけて表示する。
-  `underline` /  `u` ：テキストにアンダーラインをつけて表示する。
-  `underline2` /  `uu` ：テキストに２重アンダーラインをつけて表示する。
-  `frame` ：テキストにフレームをつけて表示する。
-  `encircle` ： テキストを囲んで表示する。
-  `overline` /  `o` ：テキストを上付線をつけて表示する。

> 補足説明：
>  `blink` や  `blink2` が機能するかどうかは、端末および端末ソフトウェアの機能と設定に
> 依存しています。
> また、使用しすぎると表示内容がかえって判読しずらくなることにも注意が必要です。

これらのスタイル属性は、重複して指定することができます。
また、スタイル属性の前に `not` を付けると、そのスタイルを無効にすることができます。 


```
 from rich.console import Console
 
 console = Console()
 console.print("Danger, Will Robinson!", 
               style="blink bold red underline on white")
 
 console.print("foo [not bold]bar[/not bold] baz", style="bold")
```

## Styleクラス
キーワード引数  `style` に与えたスタイル定義が解析されて `Style` クラスのインスタンスが作成されます。スタイル定義の解析には少し時間がかかるため、 `Style` クラスのインスタンスを作成する方が若干速くなります。しかし、Richは解析されたスタイル定義をキャッシュするため、オーバーヘッドがあるのは最初の呼び出しでのみです。

 `Style` クラスのコンストラクタとして、スタイル属性はキーワード引数として与えることができ、それらを組み合わせることができます。


```
 from rich.console import Console
 from rich.style import Style
 
 console = Console()
 danger_style = Style(color="red", blink=True, bold=True)
 console.print("Danger, Will Robinson!", style=danger_style)
```

また、 `Style` クラスのインスタンスは演算子（ `+` 、 `-` ）を使用することができるので、既存のスタイルを変更するときに便利です。


```
 from rich.console import Console
 from rich.style import Style
 
 console = Console()
 
 base_style = Style.parse("cyan")
 console.print("Hello, World", style = base_style + Style(underline=True))
```

### スタイルのテーマ
スタイル属性がコードの中にハードコーディングされていると、属性や色を変更したい場合は、保守作業の工数が増えるだけでなく、バグを混入させてしまいやすくなります。
Rich は、名前で参照できるカスタムスタイルを定義するための  `Theme` クラスを提供します。  `Theme` クラスを利用することで、スタイル属性の設定場所を集約することができ、変更する場合も1か所を修正するだけで済みます。

スタイルテーマを使用すると、コードをより意味づけすることができます。たとえば、 `warning` と名前付けされたスタイルは、 `sytle="italic magenta underline"` よりも適切に意味を表現しています。

```
 from rich.console import Console
 from rich.theme import Theme
 
 custom_theme = Theme({
     "info" : "dim cyan",
     "warning": "magenta",
     "danger": "bold red"
 })
 
 console = Console(theme=custom_theme)
 console.print("This is information", style="info")
 console.print("[warning]The pod bay doors are locked[/warning]")
 console.print("Something terrible happened!", style="danger")
```

> スタイル名の制限：
> スタイル名は次の文字のみだけで構成されている必要があります。
>  小文字英字、 ピリオド( `.` )、アンダースコアー( `_` )、ハイフォン( `-` )

### デフォルトのテーマ
 `Theme` クラスは、Richに組み込まれているデフォルトスタイルを継承します。
既存のテーマは次のコマンドで確認することができます。

 zsh
```
 % python -m rich.theme
```

新しく作成するカスタムテーマに、既存のスタイルテーマと同じスタイル名前が含まれている場合は置き換えられます。 これにより、独自のスタイルを作成するのと同じくらい簡単にデフォルトテーマをカスタマイズできます。 
たとえば、数字を強調表示したいような場合は次のようにします。


```
 from rich.console import Console
 from rich.theme import Theme
 console = Console(theme=Theme({"repr.number": "bold green blink"}))
 console.print("The total is 128")
```

Rich はスタイルを外部の構成ファイルに記述し、必要に応じて読み込むことができます。

 style_config.ini
```
 [styles]
 info = dim cyan
 warning = magenta
 danger = bold red
```

読み込むときは `Theme.read()` メソッドを使用します。

```
 from rich.console import Console
 from rich.theme import Theme
 
 custom_theme = Theme.read(path='style_config.ini')
 console = Console(theme=custom_theme)
 console.print("This is information", style="info")
 console.print("[warning]The pod bay doors are locked[/warning]")
 console.print("Something terrible happened!", style="danger")
 
```

### コンソールマークアップ
 `Console` クラスの `print()` や `log()` メソッドは、色とスタイルを設定できる簡単なマークアップをサポートしています。

#### タグ
コンソールマークアップは、[bbcode ](https://ja.wikipedia.org/wiki/BBコード) に触発されたタグ構文を使用します。 

>  `[スタイル]` text  `[/ スタイル]` 
>  `[スタイル]` text  `[/]` 

スタイルにはスタイル属性を複数設定することができます。

python
```
 from rich import print as rpint
 rprint("[bold red]alert![/bold red] Something happened")
 rprint("[bold red]Bold and red[/] not bold or red")
```

タグの終端がないときは、その文字列についてだけ、文字列の最後まで適用されます。 

python
```
 from rich import print as rprint
 rprint("[bold italic yellow on red blink]This text is impossible to read")
 rprint("This is normal text.")
```

#### link
コンソールマークアップは、次のタグ構文でハイパーリンクを出力することができます。

>  `[link = URL]` text   `[/ link]` 


```
 from rich import print as rprint
 rprint("Search on [link=](https://www.google.com]Google[/link)!")
```

端末にはハイパーリンクが表示されますが、このハイパーリンクが機能するためには、端末ソフトウェアがハイパーリンクをサポートしている必要があります。
サポートされている場合は、文字列 "Google" をクリックすると、設定されているブラウザが開きます。 ハイパーリンクをサポートしていない場合は、テキストは表示されますが、クリックすることはできません。

> Macの 場合：
> Terminal: ハイパーリンクをサポートしていません。
> 　　　　ただし、URLが表示されていれば、commandキーを押下しながらマウスダブルクリックで
>                  システムのデフォルトのブラウザでそのURLをオープンします。
> iTerm2: commandキーを押下しながらマウスクリックでハイパーリンクが機能します。

#### タグのエスケープ
場合によっては、Richがマークアップとして解釈するものを印刷したいことがあります。 タグの前にバックスラッシュ( `\` )を付けると、そのタグをエスケープできます。 


```
 from rich import print as rprint
 rprint("foo\[bar]")
```

### コンソールマークアップのレンダリング
Rich は文字列を `print()` に渡すときや、後述する `Table` クラスや `Panel` クラスのオブジェクトを文字列に埋め込むことようなときは、コンソールマークアップをレンダリングします。
コンソールマークアップは便利ですが、タグ構文が出力したい文字列と競合する場合には、無効にすることができます。
これは、 `print()` メソッド、もしくは  `Console` クラスのコンストラクターで  `markup = False` を設定することができます。

### コンソールマークアップのAPI
 `from_markup()` メソッドを呼び出すことで、文字列をスタイル付きテキストに変換できます。 `from_markup()` は出力やスタイルの追加が可能な `Text` クラスのインスタンスを返します。

## Textクラス
Richには、文字列を色やスタイル属性でマークアップするために使用できる  `Text` クラスがあります。 Rich で文字列が受け入れられる場合であれば、 `Text` インスタンスを使用することができます。
このクラスは、テキストの領域がマークアップされた文字列のようなものです。 組み込みの `str` クラスのインスタンスは不変(immutable)ですが、 `Text` インスタンスは変更可能(mutable)であり、 `Text` クラスのほとんどのメソッドは新しいインスタンスオブジェクトを返すのではなく、in-placeで動作します。つまり、そのオブジェクトそのものを返します。

### stylize()メソッド
 `stylize()` メソッドは、スタイルと、開始位置、終了位置を与えて、文字列にスタイルを適用することができます。

 text_style.py
```
 from rich.console import Console
 from rich.text import Text
 
 console = Console()
 text = Text("Hello, World!")
 text.stylize("bold red", 0, 5)
 console.print(text)
```

これを実行すると、赤の太文字で Hello (文字列の開始位置0, 終了位置5)を含む文字列が出力されます。

### append()メソッド
 `append()` メソッドを使うと、 `Text` オブジェクトに文字列にスタイルを適用した `Text` オブジェクトを追加することができます。

 text_style_append.py
```
 from rich.console import Console
 from rich.text import Text
 
 console = Console()
 text = Text()
 text.append("Hello", style="bold red")
 text.append(" World!")
 console.print(text)
```

### assemble()メソッド
個別の `Text` オブジェクトを使って、別の `Text` オブジェクトを作成することは一般的です。
Rich には文字列や文字列とStyleのペアを組み合わせて `Text` インスタンスを返す `assemble()` を提供します。 
次のコードは、 `append()` メソッドのサンプルコードと等価です。

 text_style_assemble.py
```
 from rich.console import Console
 from rich.text import Text
 
 console = Console()
 text = Text()
 text = Text.assemble(("Hello", "bold red"), " World!")
 console.print(text)
```

### Textクラスのパラメタ
 `Text` クラスには、コンストラクターで設定できるいくつかのパラメーターがあります。
次のパラメタを指定してテキストの表示方法を変更することができます。

-  `justify` ：整列と両揃えの設定を指示します。
  - これは、 `left` 、 `right` 、 `center` 、 `full` のいずれかを設定します。
-  `overflow` ：表示サイズを超えた文字列の表示設定を指示します。
  - これは、 `fold` 、 `crop` 、 `ellipsis` のいずれかを設定します。
-  `no_wrap` 表示サイズを超えた文字列の折返しをしません。
-  `tab_size` ：タブの空白文字数を指定します。

 `Text` インスタンスは、Rich APIのほぼすべての場所で通常の文字列の代わりに使用できます。このため、他のRichのレンダリング可能なオブジェクトで、テキストのレンダリング方法を制御することができます。
次のコードは、 `rich.panel.Panel` クラスのインスタンスオブジェクトの中のテキストを右揃えにします。

 text_attribute.py
```
 from rich import print
 from rich.panel import Panel
 from rich.text import Text
 panel = Panel(Text("Hello", justify="right"))
 print(panel)
```

![](https://gyazo.com/63848d22911732f49fbc15e5190c2fea.png)

### 強調表示
Richは、 `print()` や  `log()` が出力するテキストで、特定のパターンにスタイルを適用できます。 デフォルト設定では、Richは数値( `number` )、文字列( `strings` )、コレクション( `collections` )、ブール値( `bool` )、 `None` 、およびファイルパス、URL、UUID などのパターンを強調表示(ハイライト: Highlight)することができます。

強調表示を無効にするためには、 `print()` や  `log()` で  `highlight=False` を設定することができます。 `Console` クラスのコンストラクターで  `highlight=False` を設定すると、インスタンスオブジェクト全体に対して設定することができます。
コンストラクターで強調表示を無効にしたときでも、 `print()` や  `log()` で  `highlight=True` を使用して強調表示を有効にすることができます。

### 強調表示のカスタマイズ
Rich は、デフォルトの強調表示を変更することができます。 この最も簡単な方法は、正規表現のリストに一致するテキストにスタイルを適用する `RegexHighlighter` クラスを継承したクラスを作成することです。

次のコードは、メールアドレスのテキストを強調表示するものです。
 custom_highligther.py
```
 from rich.console import Console
 from rich.highlighter import RegexHighlighter
 from rich.theme import Theme
 
 class EmailHighlighter(RegexHighlighter):
     """Apply style to anything that looks like an email."""
 
     base_style = "example."
     highlights = [r"(?P<email>[\w-]+@([\w-]+\.)+[\w-]+)"]
 
 
 theme = Theme({"example.email": "bold magenta"})
 highlight_emails = EmailHighlighter()
 
 console = Console(highlighter=highlight_emails, theme=theme)
 console.print("Send funds to money@example.org")
 
 console.print(highlight_emails("Send funds to money@example.org"))
```

 `RegexHighlighter` クラスのクラス変数  `highlights` は、正規表現のリストを設定します。正規表現に一致する式のグループ名には、 `base_style` 属性のプレフィックスが付けられ、一致するテキストのスタイルとして使用されます。 この例では、すべてのメールアドレスに `example.email` というスタイルが適用されます。

 `Console` クラスのコンストラクタで `highligth` を設定されていると、 `print()` で出力するすべてのテキストに強調表示が適用されます。（これはデフォルトの動作です）。 インスタンスを呼び出し可能オブジェクトとして使用し、結果を出力することで、より詳細なレベルで強調表示を使用することもできます。 

 `RegexHighlighter` は非常に強力ですが、ベースクラスの `Highlighter` クラスを継承して、強調表示のカスタムスキームを実装することもできます。 

 custom_highligther2.py
```
 from random import randint
 from rich import print
 from rich.highlighter import Highlighter
 
 class RainbowHighlighter(Highlighter):
     def highlight(self, text):
         for index in range(len(text)):
             text.stylize(f"color({randint(16, 255)})", index, index + 1)
 
 rainbow = RainbowHighlighter()
 print(rainbow("I must not fear. Fear is the mind-killer."))
```

## ロギングハンドラー
Richは、Pythonの loggingモジュールによって書き込まれたテキストに対して、フォーマットやカラー設定ができるロギングハンドラー（ `logging handler` ) を提供します。

多くのPythonのモジュールがスタイルを設定するタグ（大括弧： `[...]` )をエスケープすることができないため、デフォルトでは `rich.logginer.RichHandler` は `logging` ではコンソールマークアップをレンダリングしません。しかし、 `RichHandler()` のコンストラクタに `markup=True` を与えると、有効にすることができます。
あるいは、キーワード引数 `extra={"markup": True}` を指定して、ログメッセージごとに有効にすることもできます。

次のコードは  `rich.logger` の設定例です。
 rich_logging.py
```
 import logging
 from rich.logging import RichHandler
 
 FORMAT = "%(message)s"
 logging.basicConfig(
     level="NOTSET",
     format=FORMAT,
     datefmt="[%X]",
     handlers=[RichHandler()]
 )
 
 log = logging.getLogger("rich")
 log.info("Hello, World!")
 
 log.error("[bold red blink]Server is shutting down![/]",
           extra={"markup": True})
```

### トレースバック
 `RichHandler` クラスは、Richの `Traceback` クラスを使用して例外を整形して出力するように構成することができます。これにより、組み込みの例外よりも多くのコンテキストが提供されます。 ロギングで整形された例外を取得するためには、 `RichHandler` クラスのコンストラクターに  `rich_tracebacks=True` を設定します。

 rich_logging_traceback.py
```
 import logging
 from rich.logging import RichHandler
 
 logging.basicConfig(
     level="NOTSET",
     format="%(message)s",
     datefmt="[%X]",
     handlers=[RichHandler(rich_tracebacks=True)]
 )
 
 log = logging.getLogger("rich")
 try:
     print(1 / 0)
 except Exception:
     log.exception("unable print!")
```

![](https://gyazo.com/77aa3cc26861ac3cb75212838a290445.png)

## Tracebackクラス
Richは、構文の強調表示とフォーマットを使用してPythonトレースバックをレンダリングすることができます。 整形されたトレースバックは、標準のPythonトレースバックよりも読みやすく、より多くのコードを表示します。

### トレースバックの出力
 `Console` クラスの `print_exception()` メソッドは、処理している現在の例外のトレースバックを出力します。

```
 try:
     do_something()
 except:
     console.print_exception()
```

Rich はデフォルトのトレースバックハンドラーとしてインストールすることができるため、キャッチされなかったすべての例外が強調表示されてレンダリングされます。
インストールは次の例ように `install()` を呼び出すだけです。

```
 from rich.traceback import install
 install()
 
 print(1 / 0)
```

![](https://gyazo.com/97f92037c241ff3c748509ff8bc7d0dd.png)

 `install()` に  `show_locals=True` を与えると、トレースバックにローカル変数の表示するようになります。他にもいくつかのパラメタを指示することができます。

## Promptクラス
Richには、プロンプトメッセージを表示して有効な応答を受信するまでユーザーからの入力を要求する、多数の `Prompt` クラスがあります。プロンプトには文字列（コンソールマークアップと絵文字コード）または `Text` オブジェクトを指定することができます。
ユーザーがテキストを入力せずにReturnキーを押した場合に返されるデフォルト値を設定できます。

 prompt_example.py
```
 from rich.prompt import Prompt
 name = Prompt.ask("Enter your name")
 print(f'Hello {name}!')
 
 name = Prompt.ask("Enter your name", default="Jack Bauer")
 print(f'Hello {name}!')
 
 name = Prompt.ask("What is [i]your[/i] [bold red]name[/]? :smiley: ")
 print(f'Hello {name}!')
```

 `show_default=False` を与えると、 `default` で与えたデフォルト値を表示しません。

### ユーザの入力を限定させる choices 
キーワード引数  `choices` に有効な選択肢の文字列をリストで与えることができます。ユーザが選択肢以外の応答をしたときには再入力を求めます。
 `show_choices=False` とすると、選択肢を表示しません。

 prompt_choices.py
```
 from rich.prompt import Prompt
 ans = Prompt.ask("Aur you sure ",
                   choices=["Yes", "No"],
                   default="Yes")
 print(f'Your answer is {ans}!')
```

この例と同じことは、 `Confirm` クラスでもできます。

 prompt_confirm.py
```
 from rich.prompt import Confirm
 
 ans = Confirm.ask("Are you sure?")
 print(f'Your answer is {ans}!')
```

### パスワード入力
 `Prompt.ask()` にキーワード引数 `password=True` を与えると、パスワード入力時などのようにユーザの入力した文字を表示しません。

 prompt_password.py
```
 from rich.prompt import Prompt
 
 while True:
     password = Prompt.ask(
         "Please enter a password [cyan](must be at least 8 characters)",
         password=True,
     )
     if len(password) >= 8:
         break
     print("[prompt.invalid]password too short")
 
 print(f"password={password!r}")
```

### ユーザの入力を数値として受け取る
 `IntPrompt` はユーザからの入力を数値として返します、
 prompt_numbers.py
```
 from rich.prompt import IntPrompt
 
 while True:
     number = IntPrompt.ask(
         ":rocket: Enter a number between [b]1[/b] and [b]10[/b]",
         default=5
     )
     if number >= 1 and number <= 10:
         break
     print(":pile_of_poo: [prompt.invalid]Number must be between 1 and 10")
 
 print(f"number={number}")
```


## Tableクラス
Richの `Table` クラスは、データを表形式で端末にレンダリングするためのさまざまな方法を提供します。 `Table` クラスのインスタンスオブジェクトを作成し、 `add_column()` メソッドで列を追加し、 `add_row()` で行を追加してから、 `Console` オブジェクトに出力します。

 table_sample.py
```
 from rich.console import Console
 from rich.table import Table
 
 table = Table(title="Star Wars Movies")
 
 table.add_column("Released", justify="right", style="cyan", no_wrap=True)
 table.add_column("Title", style="magenta")
 table.add_column("Box Office", justify="right", style="green")
 
 table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
 table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
 table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
 table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")
 
 console = Console()
 console.print(table)
```

![](https://gyazo.com/8deb6d10e8951c937924ac18394df7c5.png)

Rich、表の内容に合わせて列幅を調整し、収まらない場合はテキストを折り返してレンダリングします。 タイトルや行セル（raw cell)、にはRIch がレンダリングできるものは何でも追加することができま。
 `rich.table.box` をインポートして、 `Table` クラスのコンストラクターで、キーワード引数 `box` 設定することで、ボーダー（境界線）のスタイルを設定することができます。


```
 from rich.table import Table, box
 table = Table(title="Star Wars Movies", box=box.MINIMAL_DOUBLE_HEAD)
```

設定可能な[boxのボータースタイルは次のコマンドを実行すると確認できます。

 zsh
```
 % python -m rich.box
```

 `Table` クラスには、境界線のレンダリング方法や列のスタイルと配置など、外観を設定するための多数の構成オプションがあります。

### カラムを追加
 `Table` クラスのコンストラクターに、位置引数として文字列を与えることで、テーブルを定義することができます。
次のコードは3つの列を持つテーブルを作成するものです。
 table_clumn.py
```
 from rich.console import Console
 from rich.table import Table, Column
 
 table = Table("Released", "Title", "Box Office", title="Star Wars Movies")
 
 console = Console()
 console.print(table)
```

これはカラムのテキストのみを指定することができます。 幅やスタイルなどの他の属性を設定する場合は、 `Column` クラスを追加します。

 table_define_clumn_by_Column.py
```
 from rich.console import Console
 from rich.table import Table, Column
 
 table = Table("Released", "Title", "Box Office", title="Star Wars Movies")
 from rich.table import Column
 table = Table(
     "Released",
     "Title",
     Column(header="Box Office", justify="right"),
     title="Star Wars Movies"
 )
 
 console = Console()
 console.print(table)
```

> 補足説明：
> 原文では  `justify` の引数を  `align` と記述されていますが、これはドキュメントの誤りです。
> ソースコードには  `justify` なっています。

### ラインの追加
デフォルトでは、テーブルにはヘッダーの下にのみラインが表示されます。 すべての行の間にラインを表示する場合は、 `Table` クラスのコンストラクターに  `show_lines=True` を与えてインスタンスを生成します。

### Grid
 `Table` クラスは、優れたレイアウトツールにもなります。 ヘッダーとラインを無効にすることで、端末内にコンテンツを配置できます。 
代替コンストラクタ  `grid()` は、そうしたテーブルを作成することができます。
次のコードは、端末の左端と右端の両方に1行で配置された2つのテキストを表示します。

 table_grid.py
```
 from rich import print
 from rich.table import Table
 
 grid = Table.grid(expand=True)
 grid.add_column()
 grid.add_column(justify="right")
 grid.add_row("Raising shields",
              "[bold magenta]COMPLETED [green]:heavy_check_mark:")
 
 print(grid)
```

## Paddingクラス
 `Padding` クラスは、テキストまたはその他のレンダリング可能なオブジェクトの周りに空白を追加するために使用します。
次のコードは、文字列 "Hello" という1文字のパディングで出力するものです。上下の空白行と、左右に空白が追加されます。

 padding_sample.py
```
 from rich import print
 from rich.padding import Padding
 test = Padding("Hello", 1)
 print(test)
```

 `Padding` クラスは、単一の値でだけでなく、値のタプルを使用して、パディングをより詳細に指定できます。CSSでのパディングの設定方法とよく似ています。

- 2つの値のタプル： 上/下と左/右　のパディングを設定します
- 4つの値のタプル：上、右、下、左　のパディングを設定します。 

次のコードは、テキストの上下に2行の空白行が表示され、左側と右側に4つの空白が追加されます。
 padding_sample1.py
```
 rom rich import print
 from rich.padding import Padding
 test = Padding("Hello", (2, 4))
 print(test)
```

 `Padding` クラスは、パディングとコンテンツにスタイルを適用する `style` 引数、パディングが端末全体に拡張されないようにする `expand=False` を与えることができます。

 padding_sample3.py
```
 from rich import print
 from rich.padding import Padding
 test = Padding("Hello", (2, 4), style="on blue", expand=False)
 print(test)
```

Richのすべてのレンダリング可能なオブジェクトと同様に、任意のコンテキストでパディングを使用することができます。テーブル内のアイテムを強調したい場合は、セルにパディングが1でスタイルが「赤」に設定したパディングオブジェクトを追加できます。

 padding_table.py
```
 rom rich.console import Console
 from rich.table import Table, Column
 from rich.padding import Padding
 
 table = Table("Released", "Title", "Box Office", title="Star Wars Movies")
 world = Padding("Hello", 1, style="red", expand=False)
 table.add_row("Hello", world, "Python")
 
 console = Console()
 console.print(table)
```

## Panelクラス
テキストまたはその他のレンダリング可能なオブジェクトの周囲に境界線を描画するには、 `Panel` クラスのコンストラクタの第１引数に対象のオブジェクトを与えてパネルを作成します。 
 panel_border.py
```
 from rich import print
 from rich.panel import Panel
 panel = Panel("Hello, [red]World!")
 print(panel)
```

 `Panel` クラスのコンストラクターに `box` 引数を設定することで、パネルのスタイルを変更できます。 使用可能なボックススタイルのリストについては、テーブルを出力するための `Table` クラスで与えるものと同じです。次のコマンドで確認することができます。
 zsh
```
 % python -m rich.box
```

パネルは端末の全幅に拡張されます。  `Panel` クラスのコンストラクターで  `expand=False` を与えるか、 `fit()` を使用してパネルを作成すると、コンテンツのサイズに適合させることができます。 
また、 `Panel` クラスのコンストラクターはタイトルを表示する  `title` 引数を与えることができます。
 panel_expand.py
```
 from rich import print
 from rich.panel import Panel
 
 panel = Panel("Hello, [red]World!", expand=False)
 print(panel)
 
 panel = Panel.fit("Hello, [red]World!", title="using fit()")
 print(panel)
```

## RanderGroupクラス
 `RenderGroup` クラスを使用すると、複数のレンダリング可能オブジェクトをグループ化することができます。パネルのようにレンダリング可能オブジェクトをひとつしか持たないコンテキストへ、グループ化したオブジェクトを与えてレンダリングできるようにすることができます。 

 randergroup_panel.py
```
 from rich import print
 from rich.console import RenderGroup
 from rich.panel import Panel
 
 panel_group = RenderGroup(
     Panel("Hello", style="on blue"),
     Panel("World", style="on red"),
 )
 panel = Panel(panel_group)
 print(panel)
```

グループ内のレンダリング可能オブジェクトが何かを事前に知っている場合に便利です。レンダリング可能オブジェクトの数が多い場合、または動的である場合は、配置が面倒になる可能性があります。 Richは、こうした状況を支援するための  `@render_group()` デコレータを提供します。 デコレータは、レンダラブルのイテレータからレンダーグループを構築します。 

 randergroup_decorator.py
```
 rom rich import print
 from rich.console import render_group
 from rich.panel import Panel
 
 @render_group()
 def get_panels():
     yield Panel("Hello", style="on blue")
     yield Panel("World", style="on red")
 
 panel = Panel(get_panels())
 print(panel)
```


## Cloumnsクラス
Richは、 `Columns` クラスを使用して、テキストまたはその他のレンダリング可能オブジェクトを適切なカラム（列）にレンダリングできます。 使用するには、イテラブルのレンダリング可能オブジェクトを使用して `Columns` クラスのインスタンスを作成して、 `Console` に出力します。

次のコードは、ディレクトリの内容を一覧表示するものです。
 columns_sample.py
```
 import os
 import sys
 
 from rich import print
 from rich.columns import Columns
 
 if len(sys.argv) < 2:
     print("Usage: python columns.py DIRECTORY")
 else:
     directory = os.listdir(sys.argv[1])
     columns = Columns(directory, equal=True, expand=True)
     print(columns)
```

 clumns_sample.py
```
 """
 This example shows how to display content in columns.
 
 The data is pulled from https://randomuser.me
 """
 
 import json
 from urllib.request import urlopen
 
 from rich.console import Console
 from rich.columns import Columns
 from rich.panel import Panel
 
 
 def get_content(user):
     """Extract text from user dict."""
     country = user["location"]["country"]
     name = f"{user['name']['first']} {user['name']['last']}"
     return f"[b]{name}[/b]\n[yellow]{country}"
 
 console = Console()
 users = json.loads(urlopen("https://randomuser.me/api/?results=30").read())["results"]
 console.print(users, overflow="ignore", crop=False)
 user_renderables = [Panel(get_content(user), expand=True) for user in users]
 console.print(Columns(user_renderables))
```

## Liveクラス
 `Live` クラスは、レンダリング可能なオブジェクトをストリーミング更新させて表示することができます。
ライブディスプレイ(Live DIsplay)のデモは次のコマンドを実行すると見ることができます。

 zsh
```
 % python -m rich.live
```

省略記号（ `…` ）が表示されている場合は、端末の高さがテーブル全体を表示するのに十分でないことを示しています。

### 基本的な使用方法
 `Live` クラスの基本的な使用法は、次の２つのケースに分類することができます。

#### 1. 同じオブジェクトを表示する（追加表示)
同じレンダリング可能オブジェクトを表示し続ける場合は、 `Live` クラスのコンストラクタに `refresh_per_second` 引数で更新秒数を指定するだけです。
端末に表示された情報は上に流れていくように表示します。

 live_same_object.py
```
 import time
 from rich.live import Live
 from rich.table import Table
 
 table = Table()
 table.add_column("Row ID")
 table.add_column("Description")
 table.add_column("Level")
 
 with Live(table, refresh_per_second=4):  # update 4 times a second to feel fluid
     for row in range(12):
         time.sleep(0.4)  # arbitrary delay
         # update the renderable internally
         table.add_row(f"{row}", f"description {row}", "[red]ERROR")
```

#### 2. 新しいオブジェクトを表示する(更新表示)
 `update()` 関数を使用して、一定の新しいレンダリング可能オブジェクトをライブディスプレイに表示することもできます。 これにより、 `Live` がレンダリングされるものを完全に変更できます。
表示されたオブジェクトが一旦消去されて、新しく出力しなおされます。

 live_new_object.py
```
 import random
 import time
 
 from rich.live import Live
 from rich.table import Table
 
 def generate_table() -> Table:
     table = Table()
     table.add_column("ID")
     table.add_column("Value")
     table.add_column("Status")
 
     for row in range(random.randint(2, 6)):
         value = random.random() * 100
         table.add_row(
             f"{row}", 
             f"{value:3.2f}", 
             "[red]ERROR" if value < 50 else "[green]SUCCESS"
         )
     return table
 
 
 with Live(refresh_per_second=4) as live:
     for _ in range(40):
         time.sleep(0.4)
         live.update(generate_table())
```

### 高度な使用方法
#### 一時的表示（Transient Display)
デフォルトでは、 `Live` コンテキストマネージャーを終了するか、または `stop()` を呼び出すと、最後に更新されたアイテムがターミナルに表示されたまま残り、カーソルが次の行に表示されます。 
 `Live` クラスのコンストラクターで  `transient=True` を与えると、コンテキストマネージャの終了時に、最後に更新されたアイテムを消去することができます。

```
 with Live(refresh_per_second=4, transient=True) as live:
     for _ in range(40):
         time.sleep(0.4)
         live.update(generate_table())
```

#### 自動更新(auto refresh)
デフォルトでは、ライブディスプレイは1秒間に4回更新されます。  `Live` クラスのコンストラクターに `refresh_per_second` 引数でリフレッシュレートを設定することができます。 更新がそれほど頻繁ではない、またはよりスムーズな感じになることがわかっている場合は、この値を4より低く設定する必要があります。

更新頻度がそれほど高くない場合は、自動更新を完全に無効にすることをお勧めします。これは、 `Live` クラスのコンストラクターで  `auto_refresh=False` を与えることで設定することができます。自動更新を無効にした場合は、 `refresh()` を呼び出すか、 `update()` に `refresh=True` を与えて実行する必要があります。

#### 垂直オーバーフロー(Vertical Overflow)
デフォルトでは、レンダリング可能オブジェクトが端末に対して大きすぎる場合、ライブディスプレイには省略記号（ `…` ）が表示されます。 これは、 `Live` クラスのコンストラクターで  `vertical_overflow` 引数を設定することで調整できます。

-  `crop` ：端末の高さまでレンダリング可能オブジェクトを表示します。 残りは隠されています。
　 `ellipsis` ：crop と同様ですが、端末の最後の行が省略記号（ `…` ）に置き換えられます。
　	デフォルトのモードです。
-  `visible` ：レンダリング可能オブジェクト全体を表示できます。
  - このモードでは表示を正しくクリアできないことに注意してください。

### 複雑な利用方法
#### 複数のレンダリング可能オブジェクトの表示
 `RenderGroup` クラスを使用して、複数のレンダリング可能オブジェクトを組み合わせて、 `Live` クラスのコンストラクターや、 `update()` メソッドに渡すことができます。
ネストされたテーブルなどのように、より複雑な構造を構築することもできます。

#### 外部のConsoleオブジェクトを利用
 `Live` クラスは、 `live.console` を介してアクセスできる `Console` オブジェクトを内部的に作成します。 この `Console` オブジェクトの `print()` や `log()` を呼び出すと、出力はライブディスプレイの上に表示されます。 

 live_console_print.py
```
 import time
 from rich.live import Live
 from rich.table import Table
 
 table = Table()
 table.add_column("Row ID")
 table.add_column("Description")
 table.add_column("Level")
 
 # update 4 times a second to feel fluid
 with Live(table, refresh_per_second=4) as live:
     for row in range(12):
         live.console.print("Working on row #{row}")
         time.sleep(0.4)
         table.add_row(f"{row}", f"description {row}", "[red]ERROR")
```

> 補足説明：
> [原文 ](https://rich.readthedocs.io/en/latest/live.html)では、 `with` 文で `as live` が欠落していますが、これはドキュメントの間違いです。
> 見てわかるように、 `live.console.print()` を実行することができません。

別のコンソールオブジェクトがあり、それを使用する場合は、 `Live` クラスのコンストラクターに渡します。 


```
 from my_project import my_console
 
 with Live(console=my_console) as live:
     my_console.print("[bold blue]Starting work!")
     ...
```

live_using_other_console.py
```
 import time
 from rich.console import Console
 from rich.live import Live
 from rich.table import Table
 
 table = Table()
 table.add_column("Row ID")
 table.add_column("Description")
 table.add_column("Level")
 
 console = Console()
 
 # update 4 times a second to feel fluid
 with Live(table, console=console, refresh_per_second=4) as live:
     for row in range(12):
         live.console.print("Working on row #{row}")
         time.sleep(0.4)
         table.add_row(f"{row}", f"description {row}", "[red]ERROR")
```

出力先をファイルに設定したファイルコンソールを渡す場合、ライブディスプレイには、ライブコンテキストが終了したときの最後のアイテムのみがファイルに出力されます。

#### 標準出力/標準エラー出力のリダイレクト
ライブディスプレイの画面が壊れないようにするために、Richは標準出力( `stdout` )と標準エラー出力( `stderr` )をリダイレクトして、組み込みの `print()` を使用できるようにします。 この機能はデフォルトで有効になっていますが、 `redirect_stdout` または `redirect_stderr` をFalseに設定することで無効にすることができます。
[table_movie.py https://github.com/willmcgugan/rich/blob/master/examples/table_movie.py] と[top_lite_simulator.py  ](https://github.com/willmcgugan/rich/blob/master/examples/top_lite_simulator.py) はライブディスプレイのデモです。

## 進行状況表示
 `Progress` クラスは、ファイルコピーなど長時間実行されるタスクの進行状況を継続的に更新される情報を表示することができます。表示される情報は自由に構成することができます。デフォルトでは、タスクの説明、プログレスバー、進捗率、推定残り時間が表示されます。

豊富な進行状況表示(Progress Display) は、それぞれにバーと進行状況情報を備えた複数のタスクをサポートします。 これを使用して、スレッドまたはプロセスで作業が行われている並列タスクを追跡することができます。
進行状況表示がどのように表示されるかを確認するためには、次のコマンドを実行してみてください。
 zsh
```
 % python -m rich.progress
```

進行状況表示はJupyterノートブックでも機能しますが、自動更新が無効になっているという警告が表示されます。  `update()` を呼び出すときは、 `refresh()` を明示的に呼び出すか、 `refresh=True` を設定する必要があります。 または、各ループで自動的に更新を行う  `track()` 関数を使用するようにします。

### 基本的な使用方法
基本的な使用法は、 `track()` 関数を呼び出すことです。この関数は、シーケンスオブジェクト（リストや `range` オブジェクトなど）と、実行中のジョブの説明をオプションとして受け入れます。  `track()` メソッドは、シーケンスから値を生成し、ループ中で進行状況情報を更新します。


```
 from rich.progress import track
 
 for n in track(range(n), description="Processing..."):
     do_work(n)
```

### 高度な使用方法
複数のタスクの情報を表示する必要がある場合、またはプログレスバーを複数する場合は、 `Progress` クラスを直接操作することができます。  `Progress` オブジェクトの `add_task()` メソッドを使用してタスクを追加し、 `update()` で進行状況を更新します。

 `Progress` クラスは、進行状況表示を自動的に開始および停止するコンテキストマネージャーとして使用するように設計されています。

 progress_sample.py
```
 import time
 from rich.progress import Progress
 
 with Progress() as progress:
 
     task1 = progress.add_task("[red]Downloading...", total=1000)
     task2 = progress.add_task("[green]Processing...", total=1000)
     task3 = progress.add_task("[cyan]Cooking...", total=1000)
 
     while not progress.finished:
         progress.update(task1, advance=0.5)
         progress.update(task2, advance=0.3)
         progress.update(task3, advance=0.9)
         time.sleep(0.02)
```

![](https://gyazo.com/56bd97e8b21e94a8521d34fa50bf9feb.png)

タスクに関連付けられている `total` のは、進行状況が100％に達するために必要なステップの数です。 このコンテキストでのステップは、読み取られたファイルのバイト数や、処理された画像の数などアプリケーションにとって意味のあるものです。

#### タスクの更新
 `Progress` クラスの  `add_task()` メソッドを呼び出すとタスクIDが返されます。 このタスクIDを使用して、作業が完了したとき、または情報が変更されたときに  `update()` を呼び出します。 通常、ステップを完了するたびに、更新を行う必要があります。 このためには、 `completed` の値を直接更新するか、現在の `completed` の値に追加される事前設定を設定します。
 `update()` メソッドは、タスクに関連付けられているキーワード引数を収集します。 これを使用して、進行状況表示に追加情報を提供します。 追加の引数は  `task.fields` に格納されます。
これは `Column` クラスで参照することができます。

#### タスクを非表示にする
タスクの `visible` の値を設定することで、タスクを表示/非表示にすることができます。 タスクはデフォルトでは表示されますが `、add_tas()` を呼び出すときに `visible=False` を与えたタスクは表示されなくなります。

#### 一時的進捗表示（Transient Progress)
通常は、 `Progress` コンテキストマネージャが終了するか、または  `stop()` を呼び出すと、最後に更新された進捗状況表示が端末に残り、カーソルが次の行に表示されます。  `Progress` クラスのコンストラクタに  `transient=True` を与えると、コンテキストマネージャの終了時に進行状況の表示を消去することもできます。


```
 with Progress(transient=True) as progress:
     task = progress.add_task("Working", total=100)
     do_work(task)
```

一時的進捗表示は、タスクが終了したときに端末に表示されている情報を最小限にしたいときに便利です。

#### 不確定な進捗状況表示
 `add_task()` メソッドでタスクを追加すると、そのタスクは自動的に開始されます。つまり、進行状況は 0％で表示され、残り時間は現在の時刻から計算されます。 進行状況の更新をする前に長い遅延がある場合、これはうまく機能しない可能性があります。 例えば、サーバーからの応答を待つか、ディレクトリ内のファイルを数えるといった、ステップ数を計算するための処理で遅延がある場合があります。 このような場合、 `add_task()` を呼び出すときに  `start=False` を与えると、何かが処理中であることをユーザーに知らせるパルスアニメーションが表示されます。 これは、不確定なプログレスバー(Indeterminate progress bar)として知られています。 ステップ数が決まったら、 `start_task()` を呼び出すとプログレスバーが0％で表示されます。あとは通常どおり `update()` を呼び出して進捗状況を更新します。

#### 自動更新
デフォルトでは、進行状況情報表示は1秒間に10回更新されます。  `Progress` クラスのコンストラクタで、 `refresh_per_second` 引数にリフレッシュレートを設定することができます。 更新頻度がそれほど高くないことがわかっている場合は、これを10未満に設定する必要があります。

更新頻度がそれほど高くない場合は、自動更新を完全に無効にすることをお勧めします。これには、コンストラクターで  `auto_refresh=False` を与えてを設定することができます。 自動更新を無効にしたときは。タスクを更新した後は  `refresh()` を呼び出す必要があります。

#### カラム
 `Progress` クラスのコンストラクターの第１引数に進行状況表示のカラムをカスタマイズすることができます。カラム、フォーマット文字列または `ProgressColumn` オブジェクトで与えます。

フォーマット文字列は、 `Taskk` インスタンスが与えられる `{task}` をレンダリングします。
例えば `"{task.description}"` はカラムにタスクの説明を表示し、
 `"{task.total} of {task.completed}"` は合計ステップのうち完了したステップ数を表示しまし。
デフォルトは、次のものとほぼ同等です。


```
 progress = Progress(
     "[progress.description]{task.description}",
     BarColumn(),
     "[progress.percentage]{task.percentage:>3.0f}%",
     TimeRemainingColumn(),
 )
```


次の `Colum` オブジェクトを使用することができます。

-  `BarColumn` ：プログレスバーを表示する
-  `TextColumn` ：テキストを表示する
-  `TimeRemainingColumn` ：残りの推定時間を表示する
-  `FileSizeColumn` ：進行状況をファイルサイズとして表示する（ステップはバイトだと想定）
-  `TotalFileSizeColumn` ：合計ファイルサイズを表示する（ステップがバイトであると想定）
-  `DownloadColumn` ：ダウンロードの進行状況を表示する（ステップがバイトであると想定）
-  `TransferSpeedColumn` ：転送速度を表示する（ステップがバイトであると想定）
-  `SpinnerColumn` ：スピナーアニメーションを表示する
-  `RenderableColumn` ：カラムに任意のレンダリング可能オブジェクトを表示する

独自のカラムを実装するためには、 `Progress` クラスを継承したクラスを作成して、他のカラムと同じように使用します。

#### print()/log()
 `Progress` クラスは、 `progress.console` を介してアクセスできる `Console` オブジェクトを内部的に作成します。 この `Console` オブジェクトの `print()` や `log()` を呼び出すことで、進行状況表示の上にオブジェクトが出力されます。


```
 with Progress() as progress:
     task = progress.add_task(total=10)
     for job in range(10):
         progress.console.print("Working on job #{job}")
         run_job(job)
         progress.advance(task)
```

別の `Console` オブジェクトを使用したい場合は、 `Progress` クラスのコンストラクタで `console` 引数に与えます。


```
 from my_project import my_console
 
 with Progress(console=my_console) as progress:
     my_console.print("[bold blue]Starting work!")
     do_work(progress)
```


#### 標準出力/標準エラー出力のリダイレクト
進捗状況表示の画面が壊れないようにするために、Richは標準出力( `stdout` )と標準エラー出力( `stderr` )をリダイレクトして、組み込みの `print()` を使用できるようにします。 この機能はデフォルトで有効になっていますが、 `redirect_stdout` または `redirect_stderr` をFalseに設定することで無効にすることができます。

#### カスタマイズ
 `Progress` クラスの進行状況表示をカスタマイズしたい場合は、 `get_renderables()` メソッドをオーバーライドすることができます。
次のコードはクラスは進行状況表示の周りにパネルをレンダリングします。

```
 from rich.panel import Panel
 from rich.progress import Progress
 
 class MyProgress(Progress):
     def get_renderables(self):
         yield Panel(self.make_tasks_table(self.tasks))
```

進行状況表示を使用したアプリケーションのデモは、[downloader.py ](https://github.com/willmcgugan/rich/blob/master/examples/downloader.py) を参照してください。このスクリプトは、プログレスバー、転送速度、ファイルサイズを進行状況表示をして、複数のファイルを同時にダウンロードすることができます。


## Markdown クラス
Richは、Markdownをコンソールにレンダリングできます。 Markdownをレンダリングするには、 `Markdown` オブジェクトを作成して、それを `Console` オブジェクトに出力します。 Markdownは、コマンドラインアプリケーションにリッチコンテンツを追加するための優れた方法です。
使用例は次のとおりです。
 markdown_smaple.py
```
 MARKDOWN = """
 # This is an h1
 
 Rich can do a pretty *decent* job of rendering markdown.
 
 1. This is a list item
 2. This is another list item
 """
 from rich.console import Console
 from rich.markdown import Markdown
 
 console = Console()
 md = Markdown(MARKDOWN)
 console.print(md)
```

![](https://gyazo.com/417e1770579c5f795d9a9d449150493d.png)

コードブロックは完全な構文の強調表示でレンダリングされることに注意してください！
コマンドラインから `Markdown` クラスを使用例を確認することができます。
次の例では、ターミナルにreadmeを表示します。

 zsh
```
 % curl -s -O https://raw.githubusercontent.com/iisaka51/rich/master/README.md
 % python -m rich.markdown README.md
```

Markdownのコマンドラインオプションについては次のコマンドで知ることができます。

 zsh
```
 % python -m rich.markdown -h
 usage: markdown.py [-h] [-c] [-t CODE_THEME] [-i INLINE_CODE_LEXER] [-y]
                    [-w WIDTH] [-j] [-p]
                    PATH
 
 Render Markdown to the console with Rich
 
 positional arguments:
   PATH                  path to markdown file
 
 optional arguments:
   -h, --help            show this help message and exit
   -c, --force-color     force color for non-terminals
   -t CODE_THEME, --code-theme CODE_THEME
                         pygments code theme
   -i INLINE_CODE_LEXER, --inline-code-lexer INLINE_CODE_LEXER
                         inline_code_lexer
   -y, --hyperlinks      enable hyperlinks
   -w WIDTH, --width WIDTH
                         width of output (default will auto-detect)
   -j, --justify         enable full text justify
   -p, --page            use pager to scroll output
```


## Syntaxクラス
Rich は、さまざまなプログラミング言語を行番号と共に強調表示することができます。
構文を強調表示するためには、 `Syntax` オブジェクトを作成して、 `Console` オブジェクトに出力します。

```
 from rich.console import Console
 from rich.syntax import Syntax
 
 console = Console()
 with open("syntax.py", "wt") as code_file:
     syntax = Syntax(code_file.read(), "python")
 console.print(syntax)
```

また、代替コンストラクタ `from_path()` を使用して、ディスクからコードをロードしてファイルタイプを自動検出する することもできます。
上記の例は、次のように書き直すことができます。

```
 rom rich.console import Console
 from rich.syntax import Syntax
 
 console = Console()
 syntax = Syntax.from_path("syntax.py")
 console.print(syntax)
```

### 行番号
 `Sytax` クラスのコンストラクタで `line_numbers=True` を与えると、Richは行番号のクラスをレンダリングするようになります。

```
 syntax = Syntax.from_path("syntax.py", line_numbers=True)
```

### テーマ
 `Syntax` クラスのコンストラクタ（および  `from_path()` ）は、[Pygments ](https://pygments.org/demo/) のテーマ名である  `theme` 属性を受け入れます。 また、端末によって構成されたカラーテーマを使用する特殊なケースのテーマ名  `ansi_dark` 、または  `ansi_light` も設定することができます。

### 背景色
 `Syntax` クラスのコンストラクタ  `background_color` 引数を指定することで、テーマの背景色をオーバーライドできます。 これは、スタイル定義が受け入れるのと同じ形式の文字列である必要があります。たとえば、 `red` 、 `＃ff0000` 、 `rgb(255,0,0)` などです。端末で設定されているデフォルトの背景色となる特別な値  `default` を設定することもできます。 

### Syntax CLI
 `Syntax` クラスはコマンドラインからでも使用することができます。 ファイル  `syntax.py` の構文を強調表示する方法は次のとおりです。
 zsh
```
 % python -m rich.syntax syntax.py
```

引数の詳細は次のコマンドで知ることができます。
 zsh
```
 % python -m rich.syntax -h
 usage: syntax.py [-h] [-c] [-i] [-l] [-w WIDTH] [-r] [-s] [-t THEME]
                  [-b BACKGROUND_COLOR]
                  PATH
 
 Render syntax to the console with Rich
 
 positional arguments:
   PATH                  path to file
 
 optional arguments:
   -h, --help            show this help message and exit
   -c, --force-color     force color for non-terminals
   -i, --indent-guides   display indent guides
   -l, --line-numbers    render line numbers
   -w WIDTH, --width WIDTH
                         width of output (default will auto-detect)
   -r, --wrap            word wrap long lines
   -s, --soft-wrap       enable soft wrapping mode
   -t THEME, --theme THEME
                         pygments theme
   -b BACKGROUND_COLOR, --background-color BACKGROUND_COLOR
                         Overide background color
```

### Consoleプロトコル
Richは、カスタムオブジェクトにリッチフォーマットの機能を追加するためのシンプルなプロトコルをサポートしているため、色、スタイル、およびフォーマットを使用してオブジェクトを  `print()` できます。

これをプレゼンテーションに使用したり、一般的な `__repr__` 文字列から解析するのが難しい可能性のある、デバッグ情報を表示したりします。

## Console のカスタマイズ
オブジェクトのコンソール出力をカスタマイズする最も簡単な方法は、 `__ rich__()` メソッドを実装することです。 このメソッドには引数は不要で、テキストやテーブルなど、Richのレンダリング可能オブジェクトを返す必要があります。 プレーンな文字列を返すと、コンソールマークアップとしてレンダリングされます。 
次に例を示します。

```
 class MyObject:
    def __rich__(self) -> str:
        return "[bold cyan]MyObject()"
```

この例では、 `MyObject` のインスタンスを  `print()` や  `log()` で出力すると、太字のシアンで `MyObject()` としてレンダリングされます。 特殊な構文の強調表示を追加するなどして、これをより有効に活用したいと思うでしょう。

### コンソールレンダリング
 `__rich__()` メソッドは、レンダリング可能なオブジェクトをひとつだけ制限されています。 より高度なレンダリングを行うには、レンダリングしたいクラスに  `__rich_console__()` メソッドを追加します。
 `__rich_console__()` メソッドは、 `Console` インスタンスと `ConsoleOptions` インスタンスを受け入れる必要があります。 他のレンダリング可能なオブジェクトのイテラブルオブジェクト(反復可能オブジェクト）を返す必要があります。 これは、リストなどのコンテナを返すことができることを意味しますが、一般に、 `yield` 文を使用する（つまり、メソッドをジェネレーターにする）ことで実装が簡単になります。

 `__rich_console__()` メソッドの例を次に示します。

```
 from dataclasses import dataclass
 from rich.console import Console, ConsoleOptions, RenderResult
 from rich.table import Table
 
 @dataclass
 class Student:
     id: int
     name: str
     age: int
     def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
         yield f"[b]Student:[/b] #{self.id}"
         my_table = Table("Attribute", "Value")
         my_table.add_row("name", self.name)
         my_table.add_row("age", str(self.age))
         yield my_table
```

この例では、 `Student` クラスのインスタンスを印刷すると、端末に簡単なテーブルがレンダリングされます。

### 低レベルのレンダリング
カスタムオブジェクトが端末にレンダリングされる方法を完全に制御するために、 `Segment` オブジェクトを生成することができます。  `Segment` オブジェクトは、テキストとオプションのスタイルで構成されます。 次の例では、 `MyObject` インスタンスをレンダリングするときにマルチカラーのテキストを書き込みます。

```
 class MyObject:
     def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
         yield Segment("My", Style(color="magenta"))
         yield Segment("Object", Style(color="green"))
         yield Segment("()", Style(color="cyan"))
```

### レンダリング可能オブジェクトの測定
Richは、レンダリング時にオブジェクトが占める文字数を知る必要がある場合があります。 たとえば、 `Table` クラスはこの情報を使用して、カラムの最適な大きさを計算します。 Richモジュールでレンダリング可能なオブジェクトを使用していない場合は、 `Console` オブジェクトの最大幅を受け入れ、 `Measurement` オブジェクトを返す `__rich_measure__()` メソッドを指定する必要があります。  `Measurement` オブジェクトには、レンダリングに必要な最小文字数と最大文字数が含まれている必要があります。

たとえば、チェス盤をレンダリングする場合、レンダリングには最低8文字が必要です。 最大値は、使用可能な最大幅として残すことができます（ボードが中央に配置されていると仮定）。

```
 class ChessBoard:
     def __rich_measure__(self, console: Console, max_width: int) -> Measurement:
         return Measurement(8, max_width)
```


