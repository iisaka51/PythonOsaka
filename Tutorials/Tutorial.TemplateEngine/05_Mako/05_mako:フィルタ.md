mako:フィルタ
=================
![](https://gyazo.com/4bdf2b5b1a1690f4ec26052263276df8.png)

### フィルタ
Makoには、HTML、URI、XMLフィルタなど、多数の組み込みフィルタと、 `trim()` 関数が提供されています。これらは、パイプ記号( `|` )を使用して式の置換に追加できます。


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
- `u` ：URLフィルタ `urllib.quote_plus(string.encode('utf-8'))`を適用
- `h` ：HTMLフィルタ `markupsafe.escape(string)`を適用
- `x` ：XMLフィルタ
- `trim` ：空白のトリミング　`string.strip()`を適用
- `entity` ：該当する文字列のHTMLエンティティ参照を生成
- `str` ：Python 文字列を生成（デフォルト）
- `decode.<someencoding>` ：指定したエンコーディングでPython 文字列にデコード
- `n` ：すべてのデフォルトフィルタリングを無効

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

ページは、 `<%page>` タグの`expression_filter`引数を使用して、すべての式タグにデフォルトのフィルターセットを適用できます。

```
 <%page expression_filter="h"/>

 Escaped text:  ${"<html>some html</html>"}
```

結果は次のようになります。

```
 Escaped text: &lt;html&gt;some html&lt;/html&gt;
```

#### default_filters引数
 `expression_filter` 引数に加えて、 `Template` と `TemplateLookup` の両方に対する`default_filters`引数は、プログラムレベルですべての式タグのフィルタリングを指定できます。 この配列ベースの引数は、デフォルトの引数Noneが指定されている場合、 `disable_unicode=True` が設定されている場合を除いて、内部的に `str` に設定されます。

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

カスタムフィルターで `default_filters` を簡単に使用できるように、`imports`引数を使用してすべてのテンプレートにインポート（または他のコード）を追加することもできます。

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
すべての場合において、式内でローカルに使用される特別なnフィルターは、 `<%page>` タグおよび`default_filters`で宣言されたすべてのフィルターを無効にします。


```
 ${'myexpression' | n}
```

いかなる種類のフィルタリングも行わずに `myexpression` をレンダリングします。

```
 ${'myexpression' | n,trim}
```

トリムフィルターのみを使用して `myexpression` をレンダリングします。

 `<%page>` タグに`n`フィルタを含めると、`default_filters`のみが無効になります。 事実上、これにより、タグのフィルターがデフォルトのフィルターに追加されるのではなく、置き換えられます。

```
 <%page expression_filter="n, json.dumps"/>
 data = {a: ${123}, b: ${"123"}};
```

デフォルトのフィルターを使用して値を文字列に変換することを抑制します。これにより、 `json.dumps()` または、同等の `imports=["import json"]` は値型を考慮に入れ、数値を数値リテラルとして、文字列を文字列リテラルとしてフォーマットできます。

### defとblockのフィルタリング
 `<%def>` タグと `<%block>` タグには、指定されたフィルター関数のリストを `<%def>` の出力に適用する `filter` 引数があります。

```
 <%def name="foo()" filter="h, trim">
     <b>this is bold</b>
 </%def>
```

上記のように `filter` 属性がDefに適用されると、Defも自動的にバッファリングされます。 これについて次に説明します。

### バッファリング
mako の中心的な設計目標の1つは、スピードです。 この目的のために、テンプレート内のすべてのテキストコンテンツとそのさまざまな呼び出し可能オブジェクトは、デフォルトで、 `Context` オブジェクト内に格納されている単一のバッファーに直接パイプされます。 これは通常見逃しがちですが、特定の副作用があります。 主なものは、通常の式の構文、つまり`${somedef()}`を使用してDefを呼び出すと、関数の戻り値が生成されたコンテンツであるように見える場合があり、それが他の関数と同じようにテンプレートに配信されることです。 通常はそうではないことを除いて、他の式の置換。 `${somedef()}` の戻り値は、単に空の文字列( `''` )です。 この空の文字列を受信するまでに、 `somedef()` の出力は基になるバッファに送信されています。

たとえば、次のようなことをしている場合、この効果は必要ないかもしれません。

```
 ${" results " + somedef() + " more results "}
```
 `somedef()` 関数がコンテンツ「`somedef()`の結果」を生成した場合、上記のテンプレートは次の出力を生成します。

```
 somedef's results results more results
```
これは、式が連結の結果を返す前に `somedef()` が完全に実行されるためです。 連結は、中間式として空の文字列のみを受け取ります。

mako はこれを回避する2つの方法を提供します。 1つは、 `<%def>` タグ自体にバッファリングを適用することです。

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

そのため、 `somedef()` の内容は2番目のバッファーに送信され、2番目のバッファーはスタックからポップされ、その値が返されます。 Defの出力のバッファリングされたスピードは明らかです。

 `<%def>` の `filter` 引数も、Defをバッファリングすることに注意してください。 これは、`<%def>`の最終コンテンツを1つのバッチでエスケープ関数に配信できるようにするためです。これにより、メソッド呼び出しが減り、フィルタリング関数自体の動作がより決定論的になります。これは、次のことを行うフィルタリング関数に役立つ可能性があります。 テキスト全体に変換を適用します。

DefまたはMako呼び出し可能オブジェクトの出力をバッファリングする別の方法は、組み込みのキャプチャ関数を使用することです。 この関数は、呼び出し元によって指定されることを除いて、上記のバッファリング操作と同様の操作を実行します。


```
 ${" results " + capture(somedef) + " more results "}
```

 `capture()` 関数の最初の引数は関数自体であり、呼び出した結果ではないことに注意してください。 これは、バッファリングされた環境を設定した後、`capture()` 関数が実際にターゲット関数を呼び出すジョブを引き継ぐためです。 関数に引数を送信するには、代わりにキャプチャするために引数を送信します。

```
 ${capture(somedef, 17, 'hi', use_paging=True)}
```

上記の呼び出しは、バッファなしの呼び出しと同等です。

```
 ${somedef(17, 'hi', use_paging=True)}
```

### デコレーション
 `<%def>` のフィルターのようなものですが、より柔軟性があり、`<%def>` のデコレーター引数を使用すると、Pythonデコレーターと同じように機能する関数を作成できます。 関数は、関数を実行するかどうかを制御できます。 この関数の本来の目的は、カスタムキャッシュロジックの作成を許可することですが、他の用途もある可能性があります。

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

上記のテンプレートは、これよりも多くの空白を使用して、 `"BAR this isfooBAR"` を返します。 この関数は、それ自体が呼び出し可能なレンダー（またはそのラッパー）であり、デフォルトではコンテキストに書き込みます。 出力をキャプチャするには、`mako.runtime`モジュールで呼び出し可能な`capture()`を使用します（テンプレートではランタイムとしてのみ使用可能）。

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

デコレータは、ネストされたDefだけでなく、トップレベルのDefやブロックでも使用できます。 テンプレートAPIからトップレベルのdef、つまり `template.get_def('somedef')`  。 `render()` を呼び出す場合、デコレータは出力をコンテキストに書き込む必要があることに注意してください。つまり、最初の例のようになります。 戻り値は破棄されます。

