prompt--toolkit を使いこなそう
=================
## prompt-toolkit について
 `prompt-toolkit` を使うとテキストベース・ユーザインタフェース(TUI: Text base User Interface) を簡単に作れるようになります。
Linux系のプラットフォームだけでなく Windows でも動作します。

>TUIについて
> Terminal base User Interface あるいは Text base User Interface とも呼ばれます。

次のような機能をもっています。
- 入力中の構文の強調表示： 構文解析には Pygments を利用
- マルチライン入力編集
- 高度なコード補完
- コピー/貼り付けするテキストの選択
- カーソルの配置とスクロールに対するマウスのサポート
- コピー/貼り付けのためのテキストの選択
- 括弧で囲まれたペーストのサポート
- カーソルの位置決めとスクロールのためのマウスサポート
- 自動提案。 （ [fish http://fishshell.com/] シェルに類似）
- 複数の入力バッファ。
- （[GNU readline ](https://tiswww.case.edu/php/chet/readline/rltop.html)に類似した機能
  - EmacsとViの両方のキーバインディング 
  - 名前付きレジスタや二重グラフのようないくつかの高度なVi機能
  - 逆方向および順方向のインクリメンタルサーチ
  - Unicode でもうまく動作（日本語も問題なし）
- クロスプラットフォーム
  - Linux、OSX、FreeBSD、OpenBSD、Windowsシステムで動作
    - Windowsでは [cmder http://cmder.net/]または[conemu ](https://conemu.github.io/) などのターミナルエミュレータを使用すると良い
  - Pure Python：すべてPython で実装されている
  - すべてのPythonバージョンで動作します。
  - 少ない依存関係：Pygments、six、wcwidth に依存しています。


## インストール
拡張モジュールなので次のようにインストールします。
 bash condaの場合
```
 $ conda install -c conda-forge prompt-toolkit
 bash pipの場合
```
 $ pip install prompt-toolkit
```

## テキストの出力
 `print_formatted_text()` 関数を使うと、端末にテキストを出力することができます。
Pythonの組み込み関数の `print()` の代替として使用することができます。
 helloworld.py
```
 from prompt_toolkit import print_formatted_text as print
 
 print('Hello world')
```

ここで、 `print_formatted_text()` 関数の名前からもわかるように、テキストに色をつけて表示することができます。

## FormattedTextクラス
prompt-toolkitでは、次の方法でテキストに色をつけることができます。

- HTMLオブジェクトを作成する
- ANSIエスケープシーケンスを含むANSIオブジェクトを作成する
- （スタイル、テキスト）タプルのリストを作成する
- （pygments.Token、text）タプルのリストを作成し、それを `PygmentsTokens` でラップする

これら4種類のインスタンスオブジェクトは、 `FormattedText` オブジェクトと呼ばれます。 prompt-toolkitは、プレーンテキスト（単純な文字列）だけでなく、 `FormattedText` オブジェクトも受け付けます。

### HTMLクラス
 formattedtext.py
```
 from prompt_toolkit import print_formatted_text, HTML
 
 print_formatted_text(HTML('<b>This is bold</b>'))
 print_formatted_text(HTML('<i>This is italic</i>'))
 print_formatted_text(HTML('<u>This is underlined</u>'))
 
 # Colors from the ANSI palette.
 print_formatted_text(HTML('<ansired>This is red</ansired>'))
 print_formatted_text(HTML('<ansigreen>This is green</ansigreen>'))
 
 # Named colors (256 color palette, or true color, depending on the output).
 print_formatted_text(HTML('<skyblue>This is sky blue</skyblue>'))
 print_formatted_text(HTML('<seagreen>This is sea green</seagreen>'))
 print_formatted_text(HTML('<violet>This is violet</violet>'))
 
 # Colors from the ANSI palette.
 print_formatted_text(HTML('<aaa fg="ansiwhite" bg="ansigreen">White on green</aaa>'))
```

![](https://gyazo.com/269b180609f5c55b56d4c12c24f67349.png)

 formattedtext_html_style.py
```
 from prompt_toolkit import print_formatted_text, HTML
 from prompt_toolkit.styles import Style
 
 style = Style.from_dict({
     'aaa': '#ff0066',
     'bbb': '#44ff00 italic',
 })
 
 print_formatted_text(HTML('<aaa>Hello</aaa> <bbb>world</bbb>!'), style=style)
```

![](https://gyazo.com/5b7124fcbeec7d6eeeb566c6f603262f.png)


### ANSIクラス
prompt_toolkit のは `ANSI` クラスは、エスケープシーケンスを解析して、 `FormattedText` にマップできます。 これは、Windowsでも動作することを意味します。 
HTMLクラスで例示した"hello world" のコードを `ANSI` クラスでは次のようになります。
 formattedtext_ansi.py
```
 from prompt_toolkit import print_formatted_text, ANSI
 
 print_formatted_text(ANSI('\x1b[31mhello \x1b[32mworld'))
```

### (Style, Text）タプル
 `HTML` クラスも `ANSI` クラスも内部的には、 `(スタイル, テキスト)` タプルのリストにマップされます。  `FormattedText` クラスを使用して直接定義することもできます
これは記述がう少し増えますが、整形されたテキストを表現するためのおそらく最も強力な方法です。
 formattedtext_tuples.py
```
 from prompt_toolkit import print_formatted_text
 from prompt_toolkit.formatted_text import FormattedText
 
 text = FormattedText([
     ('#ff0066', 'Hello'),
     ('', ' '),
     ('#44ff00 italic', 'World'),
 ])
 
 print_formatted_text(text)
```

 `HTML` クラスでの例のようにスタイルに名前をつけることができます。
 formattedtext_tuples_named.py
```
 from prompt_toolkit import print_formatted_text
 from prompt_toolkit.formatted_text import FormattedText
 from prompt_toolkit.styles import Style
 
 # The text.
 text = FormattedText([
     ('class:aaa', 'Hello'),
     ('', ' '),
     ('class:bbb', 'World'),
 ])
 
 # The style sheet.
 style = Style.from_dict({
     'aaa': '#ff0066',
     'bbb': '#44ff00 italic',
 })
 
 print_formatted_text(text, style=style)
```

### Pygments (Token, text)タプル 
Pygments の  `(Token,text)` タプルのリストを `PygmentsTokens()` に与えることで色をつけることができます。
 formattedtext_pygments.py
```
 from pygments.token import Token
 from prompt_toolkit import print_formatted_text
 from prompt_toolkit.formatted_text import PygmentsTokens
 
 text = [
     (Token.Keyword, 'print'),
     (Token.Punctuation, '('),
     (Token.Literal.String.Double, '"'),
     (Token.Literal.String.Double, 'hello'),
     (Token.Literal.String.Double, '"'),
     (Token.Punctuation, ')'),
     (Token.Text, '\n'),
 ]
 
 print_formatted_text(PygmentsTokens(text))
```

 formattedtext_pygments2.py
```
 import pygments
 from pygments.token import Token
 from pygments.lexers.python import PythonLexer
 
 from prompt_toolkit.formatted_text import PygmentsTokens
 from prompt_toolkit import print_formatted_text
 
 tokens = list(pygments.lex('print("Hello")', lexer=PythonLexer()))
 print_formatted_text(PygmentsTokens(tokens))
```

prompt-toolkitには、Pygmentsと同じようにスタイルを設定するデフォルトのカラースキームがあります。色を変更する場合は、Pygmentsトークンが次のクラス名にマップされます。

 Pygments.Token とprompt_toolkitのカラー対応

| pygments.Token | prompt_toolkit classname |
|:--|:--|
| Token.Keyword | "class:pygments.keyword" |
| Token.Punctuation | "class:pygments.punctuation" |
| Token.Literal.String.Double | "class:pygments.literal.string.double" |
| Token.Text | "class:pygments.text" |
| Token | "class:pygments" |

 `pygments.literal.string.double` のようなクラス名は、次の4つのクラス名に分解されます。

-  `pygments` 
-  `pygments.literal` 
-  `pygments.literal.string` 
-  `pygments.literal.string.double` 

最終的なスタイルは、これら4つのクラス名のスタイルを組み合わせて処理されます。 したがって、これらのPygmentsトークンからスタイルを変更するには、次のようにします。

 formattedtext_pygments3.py
```
 import pygments
 from pygments.token import Token
 from pygments.lexers.python import PythonLexer
 
 from prompt_toolkit import print_formatted_text
 from prompt_toolkit.formatted_text import PygmentsTokens
 from prompt_toolkit.styles import Style
 
 style = Style.from_dict({
     'pygments.keyword': 'underline',
     'pygments.literal.string': 'bg:#00ff00 #ffffff',
 })
 
 tokens = list(pygments.lex('print("Hello")', lexer=PythonLexer()))
 print_formatted_text(PygmentsTokens(tokens), style=style)
```

### to_formatted_text()
知っておくと便利な関数は  `to_formatted_text()` です。 この関数は与えたオブジェクトを処理して `FormattedText` オブジェクトとして返します。追加のスタイルを適用することもできます。

 formattedtext_.py
```
 from prompt_toolkit.formatted_text import to_formatted_text, HTML
 from prompt_toolkit import print_formatted_text
 
 html = HTML('<aaa>Hello</aaa> <bbb>world</bbb>!')
 text = to_formatted_text(html, style='class:my_html bg:#00ff00 italic')
 
 print_formatted_text(text)
```

## prompt()
 `prompt()` 関数は、Python組み込み関数  `input()` と同様に、ユーザーに入力を求めて、その文字列を返します。

 prompt_sample.py
```
 from prompt_toolkit import prompt
 
 text = prompt('What is your name? : ')
 print(f'You said: {text}")
```

### PromptSession
 `prompt()` 関数を呼び出す代わりに、 `PromptSession` インスタンスを作成してから、 `prompt()` メソッドを呼び出すことで、ユーザに入力を求めることもできます。
これにより、一種の入力セッションが作成されます。
 prompsession_sample.py
```
 from prompt_toolkit import PromptSession
 
 # Create prompt object.
 session = PromptSession()
 
 # Do multiple input calls.
 text1 = session.prompt('Input text1:')
 text2 = session.prompt('Input text2:')
 
 print(f'text1: {text1}, text2: {text2}')
```


 `PromptSession` には、次の2つの利点があります。

- 入力履歴の共有
  - 連続する  `prompt()` 呼び出しの間は、入力履歴は保持され共有できます。
- 引数の共有：
  -  `PromptSession()` インスタンスとその  `prompt() ` メソッドは、ほぼ同じ引数を取ります。 したがって、複数の入力を要求したいが、各入力呼び出しにほぼ同じ引数が必要な場合は、それらを  `PromptSession()` インスタンスに渡してから、 `prompt()` メソッドに値を渡すこと対応できます。

### 構文の強調表示
 `prompt()` では、ユーザが入力しているときに、構文の強調表示を行うことができます。
構文の強調表示の追加は、レクサーを追加するのと同じくらい簡単です。 すべてのPygmentsレクサーは、prompt_toolkitの `PygmentsLexer` でラップした後に使用できます。  `Lexer` 抽象基本クラスを実装することにより、カスタムレクサーを作成することもできます。

 prompt_syntax_highlight.py
```
 rom pygments.lexers.html import HtmlLexer
 from prompt_toolkit.shortcuts import prompt
 from prompt_toolkit.lexers import PygmentsLexer
 
 text = prompt('Enter HTML: ', lexer=PygmentsLexer(HtmlLexer))
 print('You said: %s' % text)
```

![](https://gyazo.com/0b0d7442165e76a379ff06d8dd507a86.png)

デフォルトのPygmentsカラースキームは、prompt_toolkitのデフォルトスタイルの一部として含まれています。 レクサーと一緒に別のPygmentsスタイルを使用する場合は、次の操作を実行できます。

 prompt_syntax_highligth2.py
```
 from pygments.lexers.html import HtmlLexer
 from pygments.styles import get_style_by_name
 from prompt_toolkit.shortcuts import prompt
 from prompt_toolkit.lexers import PygmentsLexer
 from prompt_toolkit.styles.pygments import style_from_pygments_cls
 
 style = style_from_pygments_cls(get_style_by_name('monokai'))
 text = prompt('Enter HTML: ', lexer=PygmentsLexer(HtmlLexer), style=style,
               include_default_pygments_style=False)
 print('You said: %s' % text)
```

include_default_pygments_style = Falseを渡します。そうしないと、両方のスタイルがマージされ、カスタムPygmentsスタイルで色が指定されていない場合に結果がわずかに異なる可能性があるためです。

### カラー
構文の強調表示の色は、Styleインスタンスによって定義されます。 デフォルトでは、通常の組み込みスタイルが使用されますが、任意の `Style` クラスのインスタンスを  `prompt()` 関数に渡すことができます。  `Style` オブジェクトを作成する簡単な方法は、 `from_dict()` メソッドを使用することです。

 prompt_color.py
```
 from pygments.lexers.html import HtmlLexer
 from prompt_toolkit.shortcuts import prompt
 from prompt_toolkit.styles import Style
 from prompt_toolkit.lexers import PygmentsLexer
 
 our_style = Style.from_dict({
     'pygments.comment':   '#888888 bold',
     'pygments.keyword':   '#ff88ff bold',
 })
 
 text = prompt('Enter HTML: ', lexer=PygmentsLexer(HtmlLexer),
               style=our_style)
```

prompt-toolkit の `Style.from_dict()` は、Pygments の  `Style.from_dict()` と非常に似ていますが、いくつかの違いがあります。

-  `roman` 、 `sans` 、 `mono` 、 `border` オプションは無視されます。
-  `blink` 、  `noblink` 、  `reverse` 、 `noreverse` のいくつかの追加機能があります。
- 色は `#ff0000` 形式にすることができますが、組み込みのANSI色名の1つにすることもできます。 
  - その場合、それらは端末の16色パレットに直接マップされます。

### Pygmentsスタイルの利用
すべてのPygmentsスタイルクラスは、style_from_pygments_cls（）でラップされている場合にも使用できます。

pygments.styles.tango.TangoStyleなどのPygmentsスタイルを使用するとします。これは、次のように実行できます。

カスタムスタイルの作成は、次のように行うことができます。
 prompt_pygmemts_style.py
```
 from prompt_toolkit.shortcuts import prompt
 from prompt_toolkit.styles import style_from_pygments_cls, merge_styles
 from prompt_toolkit.lexers import PygmentsLexer
 
 from pygments.styles.tango import TangoStyle
 from pygments.lexers.html import HtmlLexer
 
 our_style = merge_styles([
     style_from_pygments_cls(TangoStyle),
     Style.from_dict({
         'pygments.comment': '#888888 bold',
         'pygments.keyword': '#ff88ff bold',
     })
 ])
 
 text = prompt('Enter HTML: ', lexer=PygmentsLexer(HtmlLexer),
               style=our_style)
 print(text)
```

### プロンプトメッセージにスタイルを適用
プロンプトメッセージにスタイルを適用することもできます。 これには、いくつかの `FormattedText` オブジェクトを作成する必要があります。 この方法は、 `(スタイル,テキスト)` のタプルのリストを作成することです。 次の例では、クラス名を使用してスタイルを参照します。

 prompt_style_on_promptmsg.py
```
 from prompt_toolkit.shortcuts import prompt
 from prompt_toolkit.styles import Style
 
 style = Style.from_dict({
     # User input (default text).
     '':          '#ff0066',
 
     # Prompt.
     'username': '#884444',
     'at':       '#00aa00',
     'colon':    '#0000aa',
     'pound':    '#00aa00',
     'host':     '#00ffff bg:#444400',
     'path':     'ansicyan underline',
 })
 message = [
     ('class:username', 'john'),
     ('class:at',       '@'),
     ('class:host',     'localhost'),
     ('class:colon',    ':'),
     ('class:path',     '/user/john'),
     ('class:pound',    '# '),
 ]
 
 text = prompt(message, style=style)
 print(text)
```

プロンプトメッセージは任意の種類のスタイルが適用されたテキストにすることができます。
デフォルトでは、色は256カラーパレットから取得されます。 24ビットのTrueColorが必要な場合は、 `prompt()` 関数に  `true_color=True` オプションを追加することで可能になります。


```
 text = prompt(message, style=style, true_color=True)
```



## REPLの実装
Python の REPLのようにプロンプトを表示して、ユーザからの入力を待つような処理は、
 `prompt()` で実装することができます。

 prompt_prompt_demo.py
```
 from prompt_toolkit import prompt
 
 while True:
     user_input = prompt('>>>>> ')
     print(user_input)
```
このコードは単純に文字列をエコーしているだけですが、 `default=文字列` を与えて、その文字列をはじめに表示させておくこともできます。
入力中はカーソルキーの他に、 `emacs` エディタスタイルでのカーソル移動ができます。
 `vi_mode=True` を与えると  `vi` エディタスタイルでのカーソル移動となります。

>  トリビア: emcas vs vi
> この２つのエディタには長い歴史と変遷があります。
> キーボードは利用者が長い時間接するデバイスのひとつで、
> 好みや感覚、慣れが強く影響するため、キー操作を決めるのはなかなか難しい問題です。
> こうした理由から両方のキー操作を受け付けるように開発されることがあります。
> [History of Emacs and vi Keys http://xahlee.info/kbd/keyboard_hardware_and_key_choices.html]

## ボトムライン
先の例ではどうやって入力状態から抜け出るのか示されていないので、ユーザには不親切です。そこで、最下行にメッセージを表示してみましょう。
 prompt_prompt_bottom_toolbar.py
```
 from prompt_toolkit import prompt
 
 def status_line():
     return 'To exit Ctl+C or Ctl+D.'
 
 while True:
     user_input = prompt('>>>>> ',
                         bottom_toolbar=status_line,
                         )
     print(user_input)
```

![](https://gyazo.com/cad11a5333d9e95f87bca645a2a1da0b.png)


## プロンプトメッセージを右端に配置
 `prompt()` 関数は、プロンプトメッセージを端末の右端に配置することができます。下部のツールバーを追加するのと同様に、 `rprompt` 引数を与えます。
 `rprompt` には、プレーンテキスト、 `FormattedText` 、またはいずれかを返す関数のずれかです。

 prompt_rprompt.py
```
 rom prompt_toolkit import prompt
 from prompt_toolkit.styles import Style
 
 example_style = Style.from_dict({
     'rprompt': 'bg:#ff0066 #ffffff',
 })
 
 def get_rprompt():
     return '<rprompt>'
 
 answer = prompt('> ', rprompt=get_rprompt, style=example_style)
```

![](https://gyazo.com/0fde73dc58563406fd380a8528e06775.png)

### パスワード入力
 `prompt()` に `is_password=True` を与えると、ユーザが入力した文字をアスタリスク( `*` )で置き換えて表示します。

 prompt_password.py
```
 from prompt_toolkit import prompt
 
 password = prompt('Enter password: ', is_password=True)
 print(f'Your password: {password}')
```

![](https://gyazo.com/7af5c5ec279fa67238e26a57a5406557.png)


## コマンドヒストリ
REPLにコマンドヒストリの機能を追加するためには、  `history=FileHistory()` でファイル名を与えておくと、に入力された文字列を保存して履歴を辿れるようになります。
 prompt_prompt_history.py
```
 from prompt_toolkit import prompt
 from prompt_toolkit.history import FileHistory
 
 while True:
     user_input = prompt('>>>>> ',
                         history=FileHistory('history.txt'))
     print(user_input)
```

## 自動提案
今度は、自動提案(auto suggestion) の機能を追加してみましょう。
これには、 `prompt()` の  `auto_suggest=AutoSuggestFromHistory()` を追加します。
ユーザが入力している文字列を過去の入力履歴と比べて、合致するものを薄く表示してくれるようになります。
 prompt_prompt_autosa.py
```
 from prompt_toolkit import prompt
 from prompt_toolkit.history import FileHistory
 from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
 
 while True:
     user_input = prompt('>>>>> ',
                         history=FileHistory('history.txt'),
                         auto_suggest=AutoSuggestFromHistory(),
                        )
     print(user_input)
```
![](https://gyazo.com/676ab76f61b650c8920f04b739cd1bc6.png)


## ワード補完
自動補完(Auto Completion)は、 `completer` 引数に `Completer` 抽象基本クラスのインスタンスオブジェクトを与えることで、 `WordCompleter` クラスは、そのインターフェイスを実装するコンプリーターの例です。

次のように定義すると、登録してある文字列を認識すると補完ダイアログが表示されて、
ユーザが選択できるようになります。
 prompt_wordcompleter.py
```
 from prompt_toolkit import prompt
 from prompt_toolkit.completion import WordCompleter
 
 html_completer = WordCompleter(['<html>', '<body>', '<head>', '<title>'])
 text = prompt('Enter HTML: ', completer=html_completer)
 
 print('You said: %s' % text)
```

![](https://gyazo.com/63fcf8bfc6428d14e16bf4ceb218fcb2.png)

### 複数の階層レベルでの自動補完
自動補完がその前の入力の単語に依存するコマンドラインインターフェイスがある場合があります。 例としては、ルーターやスイッチからのCLIがあります。 その場合、単純な `WordCompleter` クラスでは不十分です。  `NestedCompleter` クラスは、複数の階層レベルで補完を定義できるようになります。

 prompt_wordcompleter_nested.py
```
 from prompt_toolkit import prompt
 from prompt_toolkit.completion import NestedCompleter
 
 completer = NestedCompleter.from_nested_dict({
     'show': {
         'version': None,
         'clock': None,
         'ip': {
             'interface': {'brief'}
         }
     },
     'exit': None,
 })
 text = prompt('    # ', completer=completer)
 print('You said: %s' % text)
```


![](https://gyazo.com/f5a3940a66e35c2fc9c3615664c8152d.png)

自動補完を定義する  `dict` 型データに `None` がある場合は、それ以降のレベルでは自動補完がないことを意味します。  `dict` 型データのすべての値が `None` になる場合は、 `dict` 型を `set` 型で定義することもできます。

### より複雑な自動補完
より複雑な自動補完をさせたいときは、 `Completer` クラスを継承して拡張することで対応できます。
 prompt_autocompletion_complex.py
```
 rom prompt_toolkit import prompt
 from prompt_toolkit.completion import Completer, Completion
 
 class MyCustomCompleter(Completer):
     def get_completions(self, document, complete_event):
         yield Completion('completion', start_position=0)
 
 text = prompt('> ', completer=MyCustomCompleter())
```

 `Completer` クラスは、ドキュメントを取得して現在の  `Completion` インスタンスを生成する `get_completions()` ジェネレーターを実装する必要があります。 それぞれの補完には、テキストの一部と位置が含まれます。
位置は、カーソルの前のテキストを固定するために使用されます。 タブキーを押すと、たとえば入力の一部を小文字から大文字に変えることができます。 これは、大文字と小文字を区別しないコンプリーターにとって意味があります。 または、あいまいな完了の場合は、タイプミスを修正できます。  `start_position` に負数を与えると、指定した数の文字が削除されて置き換えられます。

### 補完候補へスタイルを適用
それぞれの補完は、補完メニューまたはツールバーがレンダリングされるときに使用されるカスタムスタイルを提供できます。 これは、各 `Completion` オブジェクトにスタイルを渡すことで可能になります。

 prompt_autocompletion_with_style.py
```
 from prompt_toolkit import prompt
 from prompt_toolkit.completion import Completer, Completion
 
 class MyCustomCompleter(Completer):
     def get_completions(self, document, complete_event):
         # Display this completion, black on yellow.
         yield Completion('completion1', start_position=0,
                          style='bg:ansiyellow fg:ansiblack')
 
         # Underline completion.
         yield Completion('completion2', start_position=0,
                          style='underline')
 
         # Specify class name, which will be looked up in the style sheet.
         yield Completion('completion3', start_position=0,
                          style='class:special-completion')
 
 text = prompt('> ', completer=MyCustomCompleter())
```

### 曖昧補完
補完候補の1つが "django_migrations" である場合、曖昧補完(Fuzzy completion)を行うと、この文字列の文字の一部である "djm" のみを入力することで、補完を行うことができます。

Prompt_toolkitには、 `FuzzyCompleter` クラスと `FuzzyWordCompleter` クラスが提供されています。これらのコンプリーターを使うことで、曖昧補完を実装することができます。 `FuzzyCompleter` オブジェクトは、任意のコンプリーターインスタンスをラップして、 `FuzzyCompleter` として返します。 `FuzzyWordCompleter` は  `FuzzyCompleter` にラップされた `WordCompleter` のように動作します。

 `prompt()` に `complete_while_typing=True` を与えると、入力中またはユーザーがTabキーを押すと、自動完了が自動的に生成されます。


```
 text = prompt('Enter HTML: ', completer=my_completer,
               complete_while_typing=True)
```

### 非同期補完
補完の生成に時間がかかる場合は、バックグラウンドスレッドでこれを行うことができます。コンプリーターを `ThreadedCompleter` でラップするか、 `prompt()` へ `complete_in_thread=True` を渡すこと実装することができます。


```
 ext = prompt('> ', completer=MyCustomCompleter(), complete_in_thread=True)
```

### 入力の検証
 `prompt()` にはバリデーターを与えることができます。 これは、入力されたデータが受け入れ可能かどうかをチェックし、受け入れられる場合にのみそれを返すコードです。 それ以外の場合は、エラーメッセージが表示され、カーソルが特定の位置に移動します。
バリデーターには `Validator` 抽象基本クラスを実装する必要があります。 これには、ドキュメントを入力として受け取り、検証が失敗したときに  `ValidationError` を発生させる `validate()` メソッドが1つだけ必要です。

 prompt_validator.py
```
 from prompt_toolkit.validation import Validator, ValidationError
 from prompt_toolkit import prompt
 
 class NumberValidator(Validator):
     def validate(self, document):
         text = document.text
 
         if text and not text.isdigit():
             i = 0
 
             # Get index of fist non numeric character.
             # We want to move the cursor here.
             for i, c in enumerate(text):
                 if not c.isdigit():
                     break
 
             raise ValidationError(message='This input contains non-numeric characters',
                                   cursor_position=i)
 
 number = int(prompt('Give a number: ', validator=NumberValidator()))
 print('You said: %i' % number)
```

![](https://gyazo.com/a1f1b7992295a317c9734212a49dc621.png)

デフォルトでは、ユーザーがEnterキーを押下したときだけ、入力データを検証しますが、 `prompt()` に  `validate_while_typing=True` を与えると、入力中にリアルタイムで検証することができます。


```
 prompt('Give a number: ', validator=NumberValidator(),
        validate_while_typing=True)
```


 `Validator` 抽象基本クラスを実装する代わりに、 `Validator.from_callable()` メソッドに、データをチェックする関数を与えることもできます。これは、ほとんどのバリデーターで、十分で簡単なものになります。

 prompt_validator_from_callable.py
```
 from prompt_toolkit.validation import Validator
 from prompt_toolkit import prompt
 
 def is_number(text):
     return text.isdigit()
 
 validator = Validator.from_callable(
     is_number,
     error_message='This input contains non-numeric characters',
     move_cursor_to_end=True)
 
 number = int(prompt('Give a number: ', validator=validator))
 print('You said: %i' % number)
```


### click.echo_via_pager との連携
 `click` モジュールの `echo_via_pager()` を使用すると、less や more などのような多数行を表示できるページャーを使用することができます。
 prompt_with_click_pager.py
```
 from prompt_toolkit import prompt
 from prompt_toolkit.history import FileHistory
 from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
 from prompt_toolkit.completion import WordCompleter
 import click
 
 SQLCompleter = WordCompleter(
                ['select', 'from', 'insert', 'update', 'delete', 'drop'],
                ignore_case=True)
 
 while True:
     user_input = prompt('SQL> ',
                         history=FileHistory('history.txt'),
                         auto_suggest=AutoSuggestFromHistory(),
                         completer=SQLCompleter,
                         )
     click.echo_via_pager(user_input)
```

長文や複雑な記述ではエディタから入力できた方が便利です。
こうした場合は、 `click.edit()` を呼び出すとよいでしょう。


### ラベルの更新処理
 `prompt()` に  `refresh_interval=秒` を与えると指定した間隔でプロンプト文字が更新されます。
 prompt_prompt_refresh.py
```
 import datetime
 from prompt_toolkit.shortcuts import prompt
 
 def get_prompt():
     now = datetime.datetime.now()
     return [
         ("bg:#008800 #ffffff", "%s:%s:%s" % (now.hour, now.minute, now.second)),
         ("bg:cornsilk fg:maroon", " Enter something: "),
     ]
 
 def main():
     result = prompt(get_prompt, refresh_interval=0.5)
     print("You said: %s" % result)
 
 if __name__ == "__main__":
     main()
```

![](https://gyazo.com/e98f17877f96af3d8e454c690cbc6f37.png)

## ダイアローグ
Prompt_toolkitには、Python だけでダイアログを表示するための高レベルAPIが付属しています。

#### メッセージボックス
ユーザに知らせるためのメッセージボックスは、 `message_dialog()` を使うと簡単に実装できます。
日本語などマルチバイト文字列はプラットフォーム依存です。
 prompt_messagebox.py
```
 from prompt_toolkit.shortcuts import message_dialog
 
 message_dialog(
     title='Example dialog',
     text='Do you want to continue?\nPress ENTER to quit.').run()
```

![](https://gyazo.com/6e65468e429aa6d520fd40cabe643dd2.png)

 `prompt_toolkit` では、ANSIやHTMLでの色やフォントサイズの指示を使用することができます、。
 prompt_messagebox_styled.py
```
 from prompt_toolkit.formatted_text import HTML
 from prompt_toolkit.shortcuts import message_dialog
 from prompt_toolkit.styles import Style
 
 # Custom color scheme.
 example_style = Style.from_dict(
     {
         "dialog": "bg:#88ff88",
         "dialog frame-label": "bg:#ffffff #000000",
         "dialog.body": "bg:#000000 #00ff00",
         "dialog shadow": "bg:#00aa00",
     }
 )
 def main():
     message_dialog(
         title=HTML(
             '<style bg="blue" fg="white">Styled</style> '
             '<style fg="ansired">dialog</style> window'
         ),
         text="Do you want to continue?\nPress ENTER to quit.",
         style=example_style,
     ).run()
 
 
 if __name__ == "__main__":
     main()
```

![](https://gyazo.com/6fbb33823e488255945e297bb3518831.png)

### YES/NOダイアログ
2者選択をさせたいようなときには、 `yes_no_dialog()` を使います。
 prompt_yesno_dialog.py
```
 from prompt_toolkit.shortcuts import yes_no_dialog
 
 def main():
     result = yes_no_dialog(
         title="Yes/No dialog example",
         text="Do you want to confirm?"
     ).run()
 
     print("Result = {}".format(result))
 
 if __name__ == "__main__":
     main()
```

![](https://gyazo.com/b33fcab62b2e12e8a7151ff4ef9464be.png)
 `yes_text` および  `no_text` に任意の文字列を指定することができます。
ただし、 `yesno_dialog()` が返すのは、真偽値だということに注意してください。
 prompt_yesno_dialog2.py
```
 from prompt_toolkit.shortcuts import yes_no_dialog
 
 def main():
     result = yes_no_dialog(
         title="Beer Select dialog",
         text="Which do you Like?",
         yes_text="IPA",
         no_text="LAGER"
     ).run()
 
     print("Result = {}".format(result))
 
 if __name__ == "__main__":
     main()
```
![](https://gyazo.com/0c94720885c9437e3de774bca4e2e2dd.png)

### ボタンダイアログ
選択肢が３つ以上あるようなときは、 `button_dialog()` を使います。
 prompt_button_dialog.py
```
 from prompt_toolkit.shortcuts import button_dialog
 
 def main():
     result = button_dialog(
         title="Button dialog example",
         text="Are you sure?",
         buttons=[("Yes", True), ("No", False), ("Maybe...", None),],
     ).run()
 
     print("Result = {}".format(result))
 
 if __name__ == "__main__":
     main()
```

![](https://gyazo.com/5a6648e8b1a542a23ab72c1217919deb.png)
選択肢はタプルのリストで `buttons` に与えます。
選択肢が多すぎて表示しきれないときは、代わりに  `Window too small....` のメッセージを表示して、選択肢リストの先頭要素で設定している値が返されます。

### ラジオリストボックス
 `radiolist_dialog()` を使うと、表示した選択肢から１つを選んでもらうラジオリストボックスを作ることができます。

 prompt_radiolistbox.py
```
 from prompt_toolkit.shortcuts import radiolist_dialog
 
 def main():
     result = radiolist_dialog(
         values=[
             ("red", "Red"),
             ("green", "Green"),
             ("blue", "Blue"),
             ("orange", "Orange"),
         ],
         title="Radiolist dialog example",
         text="Please select a color:",
     ).run()
 
     print("Result = {}".format(result))
 
 
 if __name__ == "__main__":
     main()
```

![](https://gyazo.com/c259fe95e1e84d257cbefbae0b7a4a0b.png)

### チェックリストボックス
 `checkboxlist_dialog()` を使うと、表示した選択肢から任意個数選んでもらうチェックリストボックスを作ることができます。
 prompt_checklistbox.py
```
 from prompt_toolkit.shortcuts import checkboxlist_dialog, message_dialog
 from prompt_toolkit.styles import Style
 
 result = checkboxlist_dialog(
     title="CheckboxList dialog",
     text="What would you like in your breakfast ?",
     values=[
         ("eggs", "Eggs"),
         ("bacon", "Bacon"),
         ("croissants", "20 Croissants"),
         ("daily", "The breakfast of the day"),
     ],
 ).run()
 
 selected_item = ','.join(result)
 print(f'You selected: {selected_item}')
```


![](https://gyazo.com/97323dc3f76fcc370aee685d06d003c5.png)

### インプットダイアログ
ユーザから文字列の入力を求めたいときには、  `input_dialog()` を使います。
 prompt_input_dialog.py
```
 from prompt_toolkit.shortcuts import input_dialog
 
 def main():
     result = input_dialog(
         title="Input dialog example",
         text="Please type your name:"
     ).run()
 
     print("Result = {}".format(result))
 
 if __name__ == "__main__":
     main()
```


![](https://gyazo.com/841ba88947351365569d1908cbeda7c9.png)


### パスワードダイアログ
ユーザからパスワード入力を求めたいときには  `input_dailog()` に  `password=True` を与えると、ユーザが入力した文字が表示されません。
 prompt_password_dialog.py
```
 from prompt_toolkit.shortcuts import input_dialog
 
 def main():
     result = input_dialog(
         title="Password dialog example",
         text="Please type your password:",
         password=True,
     ).run()
 
     print("Result = {}".format(result))
 
 if __name__ == "__main__":
     main()
```

![](https://gyazo.com/c717e5f7eb10df9b5c96aac0ce8afa3e.png)

### プログレスバー
 `ProgressBar` を使うと、時間がかかる処理などで経過状況を表示することができます。
次の例は、テキストで表示するものです。
 prompt_progressbar_simple.py
```
 import time
 from prompt_toolkit.shortcuts import ProgressBar
 
 with ProgressBar() as bar:
     for i in bar(range(120)):
         time.sleep(.05)
```

![](https://gyazo.com/65b478284dd7214ad901977e5151b17f.png)

スタイルやラベルなどにも対応しています。
 prompt_progessbar_styled.py
```
 from prompt_toolkit.shortcuts import ProgressBar
 from prompt_toolkit.formatted_text import HTML
 import time
 
 title = HTML('Downloading <style bg="yellow" fg="black">4 files...</style>')
 label = HTML('<ansired>some file</ansired>: ')
 
 with ProgressBar(title=title) as pb:
     for i in pb(range(800), label=label):
         time.sleep(.01)
```

![](https://gyazo.com/a67e5a67bc5f93355ef84dc5ba770290.png)

prompt_toolkit はフルスクリーンのアプリケーションを作成できるような機能もあるのですが、いま時点ではここまでとします。

参考：
　[prompt-toolkit ドキュメント ](https://python-prompt-toolkit.readthedocs.io/en/stable/)


