mako:構文
=================
![](https://gyazo.com/4bdf2b5b1a1690f4ec26052263276df8.png)

## Makoの構文


### コメント
コメントには2つの種類があります。 単一行コメントは、行の最初の非スペース文字として `##` を使用します。

```
 ## これはコメント
 ...text ...
```

複数行のコメントを記述する場合は、 `<%doc> ... text ... </%doc>` を使用します。

```
 <%doc>
     これはコメント
     複数行のコメント
 </%doc>
```

### 改行文字を無効
行の終わりに配置された円記号（“ \”）文字は、次の行に進む前に改行文字を捨てます。

```
 _tempalte="はじめの行 \
 その他の行"
```

これは次のように解釈されます。

```
 _template="はじめの行 その他の行"
```


### 式の置換
mako 式の置換をサポートしています。
テンプレートに記述した `${変数}` と記述した変数を`render()`メソッドに与えるキーワード引数として与えることができます。
ここで、Makoは、中括弧の間にあるもの( `${...}` }をすべてレンダリングします。 このため、関数呼び出しをすると、その結果がレンダリングされます。

 sample_syntax.py
```
 from mako.template import Template

 _template="""
 (1) ${headline} is a breaking news this morning.
 (2) 2 to the power of 2 is ${pow(2,2)}.
 """

 t = Template(_template)
 print(t.render(headline='NEWS HEADLINE'))
```


```
 $ python sample_syntax.py

 (1) NEWS HEADLINE is breaking news this morning.
 (2) 2 to the power of 2 is 4.
```


### 制御構造
制御構造とは、プログラムのフローを制御するすべてのものを指します。
Makoは、条件分岐、ループ、 `try...except` などのPythonの制御構造をサポートしています。
それらはすべてパーセント記号( `%` )につづけた、`%<keyword>` で始まり、その後にPython式が続き、`%end<keyword>` で閉じられます。`<keyword>` には、`if` や `for` などを与えます。
テンプレートでアクセス可能な変数は、Pythonコードが記述されている場所ならどこでも直接使用できます。

```
 % if x==5:
     this is some output
 % endif
```

 `%` は、前にテキストがない限り、行のどこにでも記述できます。 インデントは重要ではありません。 ここでは、if / elif / else、while、for、with、さらにはdefを含む、Pythonのコロン式のすべてを使用することができます。（コロン(`:`)を伴う制御文)
 `%<keyword>` と `%end<keyword>`では、`%`のあとに空白文字が複数あっての問題ありません。

 sample_control.py
```
 from mako.template import Template

 _template="""
 %　　　　　if credit:
 credit to:
 <ul>
 %for c in credit:
   <li> ${loop.index}: ${c}</li>
 %endfor
 </ul>
 %endif
 """

 t = Template(_template)
 print(t.render(credit=["You", "Me", "Us", "Them"]))
```

```
 % python sample_control.py

 credit to:
 <ul>
   <li> 0: You</li>
   <li> 1: Me</li>
   <li> 2: Us</li>
   <li> 3: Them</li>
 </ul>
```

 sample_for.py
```
 from mako.template import Template

 _template="""
 % for a in ['one', 'two', 'three', 'four', 'five']:
     % if a[0] == 't':
     its two or three
     % elif a[0] == 'f':
     four/five
     % else:
     one
     % endif
 % endfor
 """

 t = Template(_template)
 print(t.render())
```

パーセント記号( `%` )そのものを出力させたい場合は、`%%`のようにエスケープします。

```
 %% some text

     %% some more text
```

### ループコンテキスト
ループコンテキストは、構造体の％内にあるループに関する追加情報を提供します。

```
 <ul>
 % for a in ("one", "two", "three"):
     <li>Item ${loop.index}: ${a}</li>
 % endfor
 </ul>
```

ループしている反復可能オブジェクトのタイプに関係なく、次のコンテキストを使用することができます。

- `loop.index` ：常に0インデックスの反復カウント
- `loop.even` ：インデックスがループが偶数のとき`True`
- `loop.odd` ：インデックスが奇数のときに`True`
- `loop.first` ：ループが最初の反復であれば`True`

 `for` に与えるオブジェクトが `__len__()` メソッドを提供する場合は、次のコンテキストを使用することができます。

-  `loop.reverse_index` ：残っている反復のカウント
-  `loop.last` ：ループが最後の反復であれば`True`

 `for` に与えるオブジェクトが `__len__()` メソッドを持たない場合は `TypeError` になります。

### Pythonコードの記述

Makoは任意のPythonコードを `<%%>` タグで記述できます。
テンプレートとテンプレート自体の関数をそれぞれ定義します。
 `<%...%>` 内で、Pythonコードの通常のブロックを記述しています。 コードは任意のレベルの先行する空白で表示できますが、それ自体で一貫したフォーマットにする必要があります。 Makoのコンパイラは、Pythonのブロックを調整して、周囲の生成されたPythonコードと一致させます。

```
 これはテンプレート
 <%
     x = db.get_resource('foo')
     y = [z.element for z in x if x.frobnizzle==5]
 %>
 % for elem in y:
     element: ${elem}
 % endfor
```

### モジュールレベルのブロック
 `<%...%>` のバリアントは、モジュールレベルのコードブロックであり、`<%!...%>` で示されます。これらのタグ内のコードは、テンプレートの`render()`メソッド内ではなく、テンプレートのモジュールレベルで実行されます。 したがって、このコードはテンプレートのコンテキストにアクセスできず、テンプレートがメモリにロードされたときにのみ実行されます（ランタイム環境によっては、アプリケーションごとに1回、またはそれ以上の場合があります）。
テンプレーでモジュールをインポートしたいときは `<%! %> ` タグを使用してください。

```
 <%!
     import mylib
     import re

     def filter(text):
         return re.sub(r'^@', '', text)
 %>
```
 `<%! ... %>` ブロックはテンプレート内のどこでも宣言できます。 それらは、ソーステンプレートに表示される順序で、すべてのレンダリング呼び出し可能オブジェクトの上にある単一の連続したブロックで、結果のモジュールにレンダリングされます。

### テンプレートを早期終了
テンプレートまたは `<%def>` メソッドの処理を途中で停止して、これまでに蓄積したテキストだけを使用したい場合があります。 これは、Pythonブロック内でreturnステートメントを使用することで実現されます。 `return` ステートメントが空の文字列を返すことをお勧めします。これにより、Pythonのデフォルトの戻り値である `None` がテンプレートによってレンダリングされなくなります。 この戻り値は、`STOP_RENDERING` シンボルを介してテンプレートで提供されるセマンティック目的のためのものです。

```
 % if not len(records):
     No records found.
     <% return STOP_RENDERING %>
 % endif
```

もしくは

```
 <%
     if not len(records):
         return STOP_RENDERING
 %>
```
Makoの古いバージョンでは、 `STOP_RENDERING` シンボルの代わりに空の文字列を使用できます。

```
 <% return '' %>
```
