mako:タグ
=================
![](https://gyazo.com/4bdf2b5b1a1690f4ec26052263276df8.png)

## タグ
mako が提供する残りの部分はタグの形で行われます。 すべてのタグは同じ構文を使用します。これは、タグ名の最初の文字が `%` 文字であることを除いて、XMLタグに似ています。 タグは、含まれているスラッシュ文字または明示的な終了タグのいずれかによって閉じられます。

```
 <%include file="foo.txt"/>

 <%def name="foo" buffered="True">
     this is a def
 </%def>
```

すべてのタグには、タグごとに定義された一連の属性があります。 これらの属性のいくつかは必須です。 また、多くの属性は評価をサポートしています。つまり、属性テキスト内に式を `${...}` を使用して埋め込むことができます。

```
 <%include file="/foo/bar/${myfile}.txt"/>
```

属性が実行時評価を受け入れるかどうかは、タグのタイプとそのタグがテンプレートにコンパイルされる方法によって異なります。 式を貼り付けることができるかどうかを確認する最良の方法は、それを試すことです。 レクサーは、それが無効かどうかを通知します。

すべてのタグの簡単な要約は次のとおりです。

#### <%page>
このタグは、キャッシュ引数や、呼び出されたときにテンプレートが予期する引数のオプションのリストなど、テンプレートの一般的な特性を定義します。

```
 <%page args="x, y, z='default'"/>
```

または、キャッシュ特性を定義するページタグ：

```
 <%page cached="True" cache_type="memory"/>
```

現在、テンプレートごとに1つの `<%page>` タグのみが使用され、残りは無視されます。 これは将来のリリースで改善される予定ですが、今のところ、テンプレートに定義されている`<%page>`タグが1つしかないことを確認してください。そうしないと、期待する結果が得られない可能性があります。
-  `body()` メソッド：`<%page>` は、テンプレートレベルの引数とデフォルトを定義するために使用されます
- 式のフィルタリング：式nおフィルターは、 `<%page>` タグを使用してテンプレート全体のすべての式に適用できます
- キャッシング：テンプレートレベルのキャッシングを制御するオプションは、 `<%page>` タグに適用できます。

#### <%include>
他のテンプレート言語でおなじみのタグ  `<%include>` は、`file` 引数を受け入れ、そのファイルのレンダリング結果を呼び出すありふれたものです。

```
 <%include file="header.html"/>

     hello world

 <%include file="footer.html"/>

```

 `<%include>` は、読み込まれるテンプレートで受け取る引数にできる引数を与えることが受け入れます。ややこしい表現ですので、例を見てみる方が理解が速いはです。

```
 <%include file="toolbar.html" args="current_section='members', username='ed'"/>
```


#### <%def>
 `<%def>` タグは、テンプレートの他のポイントで呼び出すことができるコンテンツのセットを含むPython関数を定義します。 基本的な考え方は単純です。

```
 <%def name="myfunc(x)">
     this is myfunc, x is ${x}
 </%def>

 ${myfunc(7)}
```

 `<%def>` タグは、プレーンなPython の`def`文よりもはるかに強力です。Makoコンパイラは、通常は提供しない`%def`を備えた多くの追加サービスを提供するためです。
それは、 `def` をテンプレートのメソッドとしてエクスポートする機能、現在のコンテキスト、バッファリング/フィルタリング/キャッシングフラグ、およびコンテンツを含むdef呼び出し、自動伝播などがあります。
これにより、 `def` のパッケージを他の`def`呼び出しへの引数として送信できます（思ったほど難しくはありません）。


#### <%block>
 `<%block>` は、`<%def>`に近いタグですが、最下部のスコープですぐに実行され、無名にすることもできます。

```
 <%block filter="h">
     some <html> stuff.
 </%block>
```

Jinja2ブロックに触発された名前付きブロックは、構文的に適切な継承方法を提供します。

```
 <html>
     <body>
     <%block name="header">
         <h2><%block name="title"/></h2>
     </%block>
     ${self.body()}
     </body>
 </html>
```

#### <%namespace>
 `<%namespace>` は、MakoのPythonの `import` 文に相当します。 これにより、他のテンプレートファイルのすべてのレンダリング関数とメタデータ、プレーンなPythonモジュール、およびローカルで定義された関数の「パッケージ」にアクセスできます。

```
 <%namespace file="functions.html" import="*"/>
```

名前空間のインスタンスである `<%namespace>` によって生成される基になるオブジェクトは、現在のURI、継承構造、およびここで聞こえるほど難しくないその他のものなど、テンプレート固有の情報を参照するためにテンプレートで使用される中心的な構造です。 名前空間については、名前空間で説明しています。

#### <%inherit>
継承により、テンプレートは継承チェーンに配置されます。 これは、他の多くのテンプレート言語でよく知られている概念です。

```
 <%inherit file="base.html"/>
```

 `<%inherit>` タグを使用する場合、制御は最初に最上位の継承されたテンプレートに渡され、次に、継承されたテンプレートからコンテンツの呼び出し領域を処理する方法が決定されます。 Makoは、動的継承、コンテンツラッピング、ポリモーフィックメソッド呼び出しなど、この領域で多くの柔軟性を提供します。 継承でそれをチェックしてください。

#### <%nsname:defname>
 `<%<namespacename>:<defname>>` の形式の名前のタグを使用して、名前空間に対して任意のユーザー定義の「タグ」を作成できます。 このようなタグの閉じた形式と開いた形式は、それぞれインライン式と `<%call>` タグに相当します。

```
 <%mynamespace:somedef param="some value">
     this is the body
 </%mynamespace:somedef>
```

#### <%call>
呼び出しタグは、ユーザー定義タグの「クラシック」形式であり、上記の `<%namespacename:defname>` 構文とほぼ同等です。 このタグは、埋め込みコンテンツやその他の `def` を使用した `def` の呼び出しでも説明されています。

#### <%doc>
 `<%doc>` タグは、複数行コメントを処理します。

```
 <%doc>
     これはコメント
     複数行のコメント
 </%doc>
```

また、行の最初の非スペース文字としての `##` 記号は、単一行コメントに使用できます。

#### <%text>
このタグは、MakoレクサーによるMakoテンプレートディレクティブの通常の解析を一時停止し、本文の内容全体をプレーンテキストとして返します。 これは、Makoに関するドキュメントを作成するためによく使用されます。

```
 <%text filter="h">
     heres some fake mako ${syntax}
     <%def name="x()">${x}</%def>
 </%text>
```

### フィルタ
Makoには、HTML、URI、XMLフィルタなど、多数の組み込みフィルタと、 `trim()` 関数が提供されています。これらは、パイプ記号(`|`)を使用して式の置換に追加できます。


```
 from mako.template import Template

 _template='${"this is some text" | u}'

 t = Template(_template)
 print(t.render())
```

```
 % python  sample_escape.py
 this+is+some+text
```

上記の式は、式にURLフィルタを適用し、 `this+is+some+text` を生成します。
-  `u` ：URLフィルタ `urllib.quote_plus(string.encode('utf-8'))` を適用
-  `h` ：HTMLフィルタ `markupsafe.escape(string)`を適用
-  `x` ：XMLフィルタ
-  `trim` ：空白のトリミング　`string.strip()`を適用
-  `entity` ：該当する文字列のHTMLエンティティ参照を生成
-  `str` ：Python 文字列を生成（デフォルト）
-  `decode.<someencoding>` ：指定したエンコーディングでPython 文字列にデコード
-  `n` ：すべてのデフォルトフィルタリングを無効

複数のフィルターを適用するには、それらをコンマで区切ります。

```
 ${"<tag>いくつかの値</tag>  " | h, trim}
```

上記は `&lt; tag&gt; some value&lt; /tag&gt;` を生成し、先頭または末尾の空白は取り除かれます。 HTMLフィルタが最初に適用され、次に`trim`が適用されます。

もちろん、独自のフィルターを作成することもできます。フィルタは、単一の文字列引数を受け入れ、フィルタリングされた結果を返すPython関数です。 `|` の後の式演算子は、それらが表示されるテンプレートのローカル名前空間を利用します。つまり、エスケープ関数をローカルで定義できます。

```
 <%!
     def myescape(text):
         return "<TAG>" + text + "</TAG>"
 %>

 Here's some tagged text: ${"text" | myescape}
```

または任意のPythonモジュールから：

```
 <%!
     import myfilters
 %>

 Here's some tagged text: ${"text" | myfilters.tagfilter}
```
ページは、`%page` タグのexpression_filter引数を使用して、すべての式タグにデフォルトのフィルターセットを適用できます。

```
 <%page expression_filter="h"/>

 Escaped text:  ${"<html>some html</html>"}
```

結果は次のようになります。

```
 Escaped text: &lt;html&gt;some html&lt;/html&gt;
```

#### default_filters引数
expression_filter引数に加えて、TemplateとTemplateLookupの両方に対するdefault_filters引数は、プログラムレベルですべての式タグのフィルタリングを指定できます。 この配列ベースの引数は、デフォルトの引数Noneが指定されている場合、disable_unicode = Trueが設定されている場合を除いて、内部的に `str` に設定されます。

```
 t = TemplateLookup(directories=['/tmp'], default_filters=['unicode'])
```

通常のunicode / str関数を特定のエンコーディングに置き換えるには、デコードフィルタを次のように置き換えることができます。

```
 t = TemplateLookup(directories=['/tmp'], default_filters=['decode.utf8'])
```

default_filtersを完全に無効にするには、空のリストに設定します。

```
 t = TemplateLookup(directories=['/tmp'], default_filters=[])
```
任意の文字列名をdefault_filtersに追加して、すべての式にフィルターとして追加できます。 フィルタは左から右に適用されます。つまり、左端のフィルタが最初に適用されます。

```
 t = Template(templatetext, default_filters=['unicode', 'myfilter'])
```

カスタムフィルターでdefault_filtersを簡単に使用できるように、imports引数を使用してすべてのテンプレートにインポート（または他のコード）を追加することもできます。

```
 t = TemplateLookup(directories=['/tmp'],
                    default_filters=['unicode', 'myfilter'],
                    imports=['from mypackage import myfilter'])
```

上記は、次のようなテンプレートを生成します。

```
 # ....
 from mypackage import myfilter

 def render_body(context):
     context.write(myfilter(unicode("some text")))
```

#### nフィルターによるフィルタリングをオフにする
すべての場合において、式内でローカルに使用される特別なnフィルターは、<%page>タグおよびdefault_filtersで宣言されたすべてのフィルターを無効にします。 といった：

```
 ${'myexpression' | n}
```

いかなる種類のフィルタリングも行わずにmyexpressionをレンダリングします。

```
 ${'myexpression' | n,trim}
```

トリムフィルターのみを使用してmyexpressionをレンダリングします。

`<%page>` タグにnフィルタを含めると、default_filtersのみが無効になります。 事実上、これにより、タグのフィルターがデフォルトのフィルターに追加されるのではなく、置き換えられます。

```
 <%page expression_filter="n, json.dumps"/>
 data = {a: ${123}, b: ${"123"}};
```

デフォルトのフィルターを使用して値を文字列に変換することを抑制します。これにより、json.dumps（imports = ["import json"]または同等のものが必要）は値型を考慮に入れ、数値を数値リテラルとして、文字列を文字列リテラルとしてフォーマットできます。 。

バージョン1.0.14の新機能：nフィルターを<%page>タグで使用できるようになりました。

### defとblockのフィルタリング
 `<%def>` タグと`<%block>` タグには、指定されたフィルター関数のリストを `<%def>` の出力に適用する `filter` 引数があります。

```
 <%def name="foo()" filter="h, trim">
     <b>this is bold</b>
 </%def>
```

上記のようにfilter属性がdefに適用されると、defも自動的にバッファリングされます。 これについて次に説明します。

### バッファリング
マコの中心的な設計目標の1つは、スピードです。 この目的のために、テンプレート内のすべてのテキストコンテンツとそのさまざまな呼び出し可能オブジェクトは、デフォルトで、Contextオブジェクト内に格納されている単一のバッファーに直接パイプされます。 これは通常見逃しがちですが、特定の副作用があります。 主なものは、通常の式の構文、つまり `${somedef()}` を使用してdefを呼び出すと、関数の戻り値が生成されたコンテンツであるように見える場合があり、それが他の関数と同じようにテンプレートに配信されることです。 通常はそうではないことを除いて、他の式の置換。 `${somedef()}` の戻り値は、単に空の文字列('')です。 この空の文字列を受信するまでに、`somedef()` の出力は基になるバッファに送信されています。

たとえば、次のようなことをしている場合、この効果は必要ないかもしれません。

```
 ${" results " + somedef() + " more results "}
```

`somedef()` 関数がコンテンツ「somedefの結果」を生成した場合、上記のテンプレートは次の出力を生成します。

```
 somedef's results results more results
```

これは、式が連結の結果を返す前に `somedef()` が完全に実行されるためです。 連結は、中間式として空の文字列のみを受け取ります。

mako はこれを回避する2つの方法を提供します。 1つは、%def自体にバッファリングを適用することです。

```
 <%def name="somedef()" buffered="True">
     somedef's results
 </%def>
```

上記の定義は、次のようなコードを生成します。

```
 def somedef():
     context.push_buffer()
     try:
         context.write("somedef's results")
     finally:
         buf = context.pop_buffer()
     return buf.getvalue()
```

そのため、`somedef()` の内容は2番目のバッファーに送信され、2番目のバッファーはスタックからポップされ、その値が返されます。 defの出力のバッファリングに固有のスピードヒットも明らかです。

`%def` の `filter` 引数も、defをバッファリングすることに注意してください。 これは、`%def` の最終コンテンツを1つのバッチでエスケープ関数に配信できるようにするためです。これにより、メソッド呼び出しが減り、フィルタリング関数自体の動作がより決定論的になります。これは、次のことを行うフィルタリング関数に役立つ可能性があります。 テキスト全体に変換を適用します。

defまたはMako呼び出し可能オブジェクトの出力をバッファリングする別の方法は、組み込みのキャプチャ関数を使用することです。 この関数は、呼び出し元によって指定されることを除いて、上記のバッファリング操作と同様の操作を実行します。


```
 ${" results " + capture(somedef) + " more results "}
```

キャプチャ関数の最初の引数は関数自体であり、呼び出した結果ではないことに注意してください。 これは、バッファリングされた環境を設定した後、キャプチャ関数が実際にターゲット関数を呼び出すジョブを引き継ぐためです。 関数に引数を送信するには、代わりにキャプチャするために引数を送信します。

```
 ${capture(somedef, 17, 'hi', use_paging=True)}
```

上記の呼び出しは、バッファなしの呼び出しと同等です。

```
 ${somedef(17, 'hi', use_paging=True)}
```

### デコレーション

`%def` のフィルターのようなものですが、より柔軟性があり、`%def` のデコレーター引数を使用すると、Pythonデコレーターと同じように機能する関数を作成できます。 関数は、関数を実行するかどうかを制御できます。 この関数の本来の目的は、カスタムキャッシュロジックの作成を許可することですが、他の用途もある可能性があります。

デコレータは、ライブラリモジュールで定義されている関数などの通常のPython関数で使用することを目的としています。 ここでは、簡単にするために、テンプレートで定義されているpython関数について説明します。

```
 <%!
     def bar(fn):
         def decorate(context, *args, **kw):
             context.write("BAR")
             fn(*args, **kw)
             context.write("BAR")
             return ''
         return decorate
 %>

 <%def name="foo()" decorator="bar">
     this is foo
 </%def>

 ${foo()}
```

上記のテンプレートは、これよりも多くの空白を使用して、「BAR this isfooBAR」を返します。 この関数は、それ自体が呼び出し可能なレンダー（またはそのラッパー）であり、デフォルトではコンテキストに書き込みます。 出力をキャプチャするには、mako.runtimeモジュールで呼び出し可能な `capture()` を使用します（テンプレートではランタイムとしてのみ使用可能）。

```
 <%!
     def bar(fn):
         def decorate(context, *args, **kw):
             return "BAR" + runtime.capture(context, fn, *args, **kw) + "BAR"
         return decorate
 %>

 <%def name="foo()" decorator="bar">
     this is foo
 </%def>

 ${foo()}
```

デコレータは、ネストされたdefだけでなく、トップレベルのdefやブロックでも使用できます。 テンプレートAPIからトップレベルのdef、つまり `template.get_def('somedef').render()` を呼び出す場合、デコレータは出力をコンテキストに書き込む必要があることに注意してください。つまり、最初の例のようになります。 戻り値は破棄されます。



### 制御構造
制御構造とは、プログラムのフローを制御するすべてのものを指します。
Makoは、条件分岐、ループ、 `try...except` などのPythonの制御構造をサポートしています。
それらはすべてパーセント記号( `%` )につづけた、`%<keyword>` で始まり、その後にPython式が続き、`%end<keyword>`で閉じられます。 `<keyword>` には、 `if` や `for` などを与えます。
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

パーセント記号( `%` )そのものを出力させたい場合は、`%%` のようにエスケープします。

```
 %% some text

     %% some more text
```

### ループコンテキスト
ループコンテキストは、構造体の%内にあるループに関する追加情報を提供します。

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

- `loop.reverse_index` ：残っている反復のカウント
- `loop.last` ：ループが最後の反復であれば`True`

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
 `<%...%>` のバリアントは、モジュールレベルのコードブロックであり、`<%!...%>` で示されます。 これらのタグ内のコードは、テンプレートの `render()` メソッド内ではなく、テンプレートのモジュールレベルで実行されます。 したがって、このコードはテンプレートのコンテキストにアクセスできず、テンプレートがメモリにロードされたときにのみ実行されます（ランタイム環境によっては、アプリケーションごとに1回、またはそれ以上の場合があります）。
テンプレーでモジュールをインポートしたいときは `<%! %>` タグを使用してください。

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
テンプレートまたは `<%def>` メソッドの処理を途中で停止して、これまでに蓄積したテキストだけを使用したい場合があります。 これは、Pythonブロック内でreturnステートメントを使用することで実現されます。 `return`ステートメントが空の文字列を返すことをお勧めします。これにより、Pythonのデフォルトの戻り値である`None`がテンプレートによってレンダリングされなくなります。 この戻り値は、`STOP_RENDERING`シンボルを介してテンプレートで提供されるセマンティック目的のためのものです。

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

Makoの古いバージョンでは、STOP_RENDERINGシンボルの代わりに空の文字列を使用できます。

```
 <% return '' %>
```

## テンプレートの継承

テンプレートの継承を使用すると、2つ以上のテンプレートを継承チェーンに編成できます。継承チェーンでは、関連するすべてのテンプレートのコンテンツと機能を混在させることができます。 テンプレート継承の一般的なパラダイムは次のとおりです。テンプレートAがテンプレートBから継承する場合、テンプレートAは実行時に実行制御をテンプレートBに送信することに同意します（Aは継承テンプレートと呼ばれます）。 次に、継承されたテンプレートであるテンプレートBが、Aのどのリソースを実行するかを決定します。

実際には、このように見えます。 これが架空の継承テンプレートindex.htmlです。

 index.html
```
 ## index.html
 <%inherit file="base.html"/>

 <%block name="header">
     this is some header content
 </%block>

 this is the body content.
```

およびbase.html、継承されたテンプレート：

 base.html
```
 ## base.html
 <html>
     <body>
         <div class="header">
             <%block name="header"/>
         </div>

         ${self.body()}

         <div class="footer">
             <%block name="footer">
                 this is the footer
             </%block>
         </div>
     </body>
 </html>
```

実行の内訳は次のとおりです。

1. `index.html` がレンダリングされると、制御はすぐに`base.html`に移ります。
2. 次に、 `base.html` はHTMLドキュメントの上部をレンダリングしてから、
 `<%block name="header">` ブロックを呼び出します。これは、`self.header()`関数を呼び出します。 `index.html`は最上位のテンプレートであり、ヘッダーと呼ばれるブロックも定義しているため、`base.html`に存在するものではなく、最終的に実行されるのはこのヘッダーブロックです。
3. コントロールは `base.html` に戻ります。さらにいくつかのHTMLがレンダリングされます。
4.  `base.html` は `self.body()` を実行します。すべてのテンプレートベースの名前空間の`body()` 関数は、テンプレートの本体を参照するため、`index.html` の本体がレンダリングされます。
5.  `self.body()` 呼び出し中に `index.html` で `<%block name="header">` が検出されると、条件がチェックされます。現在継承されているテンプレート、つまり`base.html`もこのブロックを定義している場合、`<%block>` はここでは実行されません。継承メカニズムは、親テンプレートがこのブロックのレンダリングを担当していることを認識しています（実際にはすでに実行されています）。言い換えると、ブロックはその最下部のスコープでのみレンダリングされます。
6. コントロールは `base.html` に戻ります。より多くのHTMLがレンダリングされた後、
 `<%block name="footer">` 式が呼び出されます。
7. フッターブロックは `base.html` でのみ定義されているため、フッターの最上位の定義であり、実行されます。 `index.html`でもフッターが指定されている場合、そのバージョンはベースのバージョンをオーバーライドします。
8.  `base.html` はHTMLのレンダリングを終了し、テンプレートが完成して、次のようになります。


```
 <html>
     <body>
         <div class="header">
             ヘッダのコンテンツ
         </div>

         ボディーコンテンツ

         <div class="footer">
             フッターコンテンツ
         </div>
     </body>
 </html>
```

これがテンプレートの継承です。 主なアイデアは、自分自身で呼び出すメソッドは常にそのメソッドの最上位の定義に対応するということです。 Makoは実際にはPythonクラスの継承を使用してこの機能を実装していませんが、Pythonクラスでの `self` の動作は非常に優れています。 （Makoは、「継承」のメタファーをあまり真剣に受け止めていません。一般的に認識されているセマンティクスを設定するのに役立ちますが、テキストテンプレートは、実際にはオブジェクト指向のクラス構造とはあまり似ていません）。

### ブロックのネスト
継承されたテンプレートで定義された名前付きブロックは、他のブロック内にネストすることもできます。 各ブロックに付けられた名前は、継承するテンプレートを介してグローバルにアクセスできます。 ヘッダーブロックに新しいブロックタイトルを追加できます。

```
 ## base.html
 <html>
     <body>
         <div class="header">
             <%block name="header">
                 <h2>
                     <%block name="title"/>
                 </h2>
             </%block>
         </div>

         ${self.body()}

         <div class="footer">
             <%block name="footer">
                 this is the footer
             </%block>
         </div>
     </body>
 </html>
```

継承するテンプレートは、ヘッダーとタイトルのいずれかまたは両方に個別に名前を付けることも、ネストすることもできます。

 index.html
```
 ## index.html
 <%inherit file="base.html"/>

 <%block name="header">
     this is some header content
     ${parent.header()}
 </%block>

 <%block name="title">
     this is the title
 </%block>

 this is the body content.
```

ヘッダーを上書きするときに、独自のヘッダーブロックに加えて、親のヘッダーブロックを呼び出すために、追加の呼び出し `$ {parent.heade()}` を追加したことに注意してください。

### 名前付きブロックを複数回レンダリング
名前付きブロックは `<%def>` と同じであり、いくつかの異なる使用規則があることを思い出してください。 名前付きセクションの1つを明確に呼び出すことができます。たとえば、ページのタイトルなど、複数回使用されるセクションです。


```
 <html>
     <head>
         <title>${self.title()}</title>
     </head>
     <body>
     <%block name="header">
         <h2><%block name="title"/></h2>
     </%block>
     ${self.body()}
     </body>
 </html>
```

上記の場合、継承テンプレートは `<%block name="title">` を1回だけ定義でき、`<title>`セクションと`<h2>`の両方のベーステンプレートで使用されます。

しかし、Defsはどうですか？
前の例では、 `<%block>` タグを使用して、オーバーライドするコンテンツの領域を生成しました。 Mako 0.4.1より前のバージョンでは、`<%def>` タグを利用していました。結局のところ、名前付きブロックと `<%def>` タグはほとんど互換性があります。 `def`は単にそれ自体を自動的に呼び出さず、より柔軟でPython自体に似ているが、レイアウトにはあまり適していない、より自由な名前付けとスコープのルールを持っています。 defを使用したこの章の最初の例は次のようになります。

```
 ## index.html
 <%inherit file="base.html"/>

 <%def name="header()">
     this is some header content
 </%def>

 this is the body content.
```

そして、継承される  `base.html` は次のようになります。

```
 ## base.html
 <html>
     <body>
         <div class="header">
             ${self.header()}
         </div>

         ${self.body()}

         <div class="footer">
             ${self.footer()}
         </div>
     </body>
 </html>

 <%def name="header()"/>
 <%def name="footer()">
     this is the footer
 </%def>
```

上記では、定義と呼び出しが一度にではなく2つの別々の場所で定義されるという点で、defがブロックとは異なることを示しています。 2つを組み合わせると、ブロックとほぼ同じように実行できます。

```
 <div class="header">
     <%def name="header()"></%def>${self.header()}
 </div>
```

この種の使用法では、`<%block>` は明らかに `<%def>` よりも合理化されています。 さらに、 `<%def>` を使用した上記の「インライン」アプローチは、ネストでは機能しません。


```
 <head>
     <%def name="header()">
         <title>
         ## this won't work !
         <%def name="title()">default title</%def>${self.title()}
         </title>
     </%def>${self.header()}
 </head>
```

上記の場合、`title()` defは、def内のdefであるため、テンプレートのエクスポートされた名前空間の一部ではなく、selfの一部にもなりません。 継承されたテンプレートがトップレベルで独自のタイトル定義を定義した場合、それは呼び出されますが、上記の「デフォルトのタイトル」は、何があっても自分自身にはまったく存在しません。 これが期待どおりに機能するためには、代わりに次のように言う必要があります。

```
 <head>
     <%def name="header()">
         <title>
         ${self.title()}
         </title>
     </%def>${self.header()}

     <%def name="title()"/>
 </head>
```

つまり、タイトルは他のdefの外部で定義されているため、自己名前空間にあります。 それは機能しますが、定義はレンダリングのポイントから潜在的に遠く離れている必要があります。

名前付きブロックは、ネストに関係なく、常に自己名前空間に配置されるため、この制限は解除されます。

```
 ## base.html
 <head>
     <%block name="header">
         <title>
         <%block name="title"/>
         </title>
     </%block>
 </head>
```

上記のテンプレートはヘッダー内のタイトルを定義し、継承テンプレートは、使用するために、相互にネストされているかどうかに関係なく、任意の構成で一方または両方を定義できます。

```
 ## index.html
 <%inherit file="base.html"/>
 <%block name="title">
     the title
 </%block>
 <%block name="header">
     the header
 </%block>
```

したがって、 `<%block>` タグは、ネストされたブロックが外部で使用できないという制限を解除しますが、これを実現するには、単一のテンプレート内のすべてのブロック名がテンプレート内でグローバルに一意である必要があるという制限を追加します。  `<%block>` を `<%def>` 内で定義することはできません。これは、 `<%def>` よりも具体的なユースケースに適した、より制限されたタグです。

次の名前空間を使用してコンテンツラッピングを生成する
3つ以上のテンプレートにまたがる継承チェーンがある場合があります。または、そうではないかもしれませんが、追加の継承されたテンプレートをチェーンの途中に挿入してスムーズに統合できるようにシステムを構築したいと考えています。各テンプレートが本体内でのみレイアウトを定義する場合は、`self.body()` を呼び出して、継承するテンプレートの本体を取得することはできません。これは、最上位の本体にすぎないためです。次のテンプレートの本体を取得するには、名前空間nextを呼び出します。これは、現在のテンプレートの直後にあるテンプレートの名前空間です。

`self.body()` を呼び出すbase.htmlの行を、代わりに `next.body()` を呼び出すように変更しましょう。

```
 ## base.html
 <html>
     <body>
         <div class="header">
             <%block name="header"/>
         </div>

         ${next.body()}

         <div class="footer">
             <%block name="footer">
                 this is the footer
             </%block>
         </div>
     </body>
 </html>
```

また、base.htmlから継承するlayout.htmlという中間テンプレートを追加しましょう。

```
 ## layout.html
 <%inherit file="base.html"/>
 <ul>
     <%block name="toolbar">
         <li>selection 1</li>
         <li>selection 2</li>
         <li>selection 3</li>
     </%block>
 </ul>
 <div class="mainlayout">
     ${next.body()}
 </div>
```

そして最後に、代わりにlayout.htmlから継承するようにindex.htmlを変更します。

```
 ## index.html
 <%inherit file="layout.html"/>

 ## .. rest of template
```

この設定では、`next.body()` を呼び出すたびに、継承チェーン内の次のテンプレートの本体がレンダリングされます（base.html-> layout.html-> index.htmlと記述できます）。 制御は引き続き最初に最下部のテンプレートbase.htmlに渡され、selfは特定の定義の最上位の定義を参照します。

得られる出力は次のようになります。

```
 <html>
     <body>
         <div class="header">
             this is some header content
         </div>

         <ul>
             <li>selection 1</li>
             <li>selection 2</li>
             <li>selection 3</li>
         </ul>

         <div class="mainlayout">
         this is the body content.
         </div>

         <div class="footer">
             this is the footer
         </div>
     </body>
 </html>
```

上記のように、base.htmlの<html>、<body>、ヘッダー/フッターのレイアウト、`layout.html` の`<ul>` と `mainlayout` セクション、`index.html` の本体とそのオーバーライドがあります。 ヘッダー定義 `layout.html` テンプレートは、 `base.html` が何も変更することなく、チェーンの中央に挿入されます。 次の名前空間がないと、 `index.html` の本体しか使用できませんでした。 `layout.html` の本文コンテンツを呼び出す方法はありません。

親の名前空間を使用して定義を拡張する
次に呼び出される親の反対である、他の継承固有の名前空間を見てみましょう。 parentは、現在のテンプレートの直前にあるテンプレートの名前空間です。 この名前空間の便利な点は、defまたはblocksがオーバーライドされたバージョンを呼び出すことができることです。 これは思ったほど難しくはなく、Pythonでsuperキーワードを使用するのと非常によく似ています。 `index.html` を変更して、`layout.html` のツールバー関数によって提供される選択のリストを拡張しましょう。

```
 ## index.html
 <%inherit file="layout.html"/>

 <%block name="header">
     this is some header content
 </%block>

 <%block name="toolbar">
     ## call the parent's toolbar first
     ${parent.toolbar()}
     <li>selection 4</li>
     <li>selection 5</li>
 </%block>

 this is the body content.
```

上記では、継承されたテンプレート `layout.html` 内のツールバーの定義をオーバーライドすることを目的とした `toolbar()` 関数を実装しました。 ただし、`layout.html` のコンテンツも必要なので、コンテンツが必要なときはいつでも、この場合は独自の選択を追加する前に、親名前空間を介して呼び出します。 したがって、全体の出力は次のようになります。

```
 <html>
     <body>
         <div class="header">
             this is some header content
         </div>

         <ul>
             <li>selection 1</li>
             <li>selection 2</li>
             <li>selection 3</li>
             <li>selection 4</li>
             <li>selection 5</li>
         </ul>

         <div class="mainlayout">
         this is the body content.
         </div>

         <div class="footer">
             this is the footer
         </div>
     </body>
 </html>
```

これで、テンプレート継承忍者になりました。

テンプレートの継承で `<%include>` を使用する
混乱の一般的な原因は、`<%include>` タグの動作であり、多くの場合、テンプレート継承内での相互作用と関連しています。 `<%include>` タグを理解するための鍵は、それが動的であるということです。ランタイム、インクルード、静的インクルードではありません。 `<%include>` は、テンプレートのレンダリング時にのみ処理され、継承のセットアップ時には処理されません。参照されるテンプレートは、現在の継承構造にリンクされていない完全に別個のテンプレートとして完全に実行されます。

一方、タグが静的インクルードである場合、これにより、インクルードされたテンプレート内のソースが呼び出し元のテンプレートと同じ継承コンテキスト内で相互作用できるようになりますが、現在Makoには静的インクルード機能がありません。

実際には、これは、 `<%include>` ファイルで定義された `<%block>` 要素が、呼び出し元テンプレートの対応する `<%block>` 要素と相互作用しないことを意味します。

よくある間違いは次のとおりです。

```
 ## partials.mako
 <%block name="header">
     Global Header
 </%block>

 ## parent.mako
 <%include file="partials.mako">

 ## child.mako
 <%inherit file="parent.mako">
 <%block name="header">
     Custom Header
 </%block>
```

上記では、partials.makoのインクルードを介してparent.makoに存在する同じブロックをオーバーライドした結果として、child.makoで宣言された「header」ブロックが呼び出される可能性があると予想される場合があります。 しかし、そうではありません。 代わりに、parent.makoはpartials.makoを呼び出し、partials.makoはpartials.makoの「ヘッダー」を呼び出し、レンダリングを終了します。 child.makoからは何もレンダリングされません。 child.makoの「header」ブロックとpartials.makoの「header」ブロックの間に相互作用はありません。

代わりに、parent.makoは継承構造を明示的に指定する必要があります。 partials.makoの特定の要素を呼び出すために、名前空間として呼び出します。

```
 ## partials.mako
 <%block name="header">
     Global Header
 </%block>

 ## parent.mako
 <%namespace name="partials" file="partials.mako"/>
 <%block name="header">
     ${partials.header()}
 </%block>

 ## child.mako
 <%inherit file="parent.mako">
 <%block name="header">
     Custom Header
 </%block>
```

上記の場合、parent.makoは、child.makoが参加する継承構造を示しています。 partials.makoは、名前ごとに使用できる定義/ブロックのみを定義します。

別のシナリオを以下に示します。これにより、child.makoドキュメントに対して両方の「SectionA」ブロックがレンダリングされます。

```
 ## base.mako
 ${self.body()}
 <%block name="SectionA">
     base.mako
 </%block>

 ## parent.mako
 <%inherit file="base.mako">
 <%include file="child.mako">

 ## child.mako
 <%block name="SectionA">
     child.mako
 </%block>
```

解像度は似ています。 `<%include>` を使用する代わりに、名前空間を使用してchild.makoのブロックを呼び出します。

 html
```
 ## parent.mako
 <%inherit file="base.mako">
 <%namespace name="child" file="child.mako">

 <%block name="SectionA">
     ${child.SectionA()}
 </%block>
```

### 継承可能な属性
NamespaceオブジェクトのNamespace.attrアクセサーを使用すると、テンプレートで宣言されたモジュールレベルの変数にアクセスできます。 self.attrにアクセスすることで、`<%!...%>` で宣言されている継承チェーンから通常の属性にアクセスできます。

```
 <%!
     class_ = "grey"
 %>

 <div class="${self.attr.class_}">
     ${self.body()}
 </div>
```
次のように、継承するテンプレートがclass_をオーバーライドして「白」になる場合。

```
 <%!
     class_ = "white"
 %>
 <%inherit file="parent.html"/>

 This is the body
```

出力は次のようになります。

```
 <div class="white">
     This is the body
 </div>
```
