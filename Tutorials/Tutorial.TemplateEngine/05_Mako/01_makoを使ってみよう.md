makoを使ってみよう
=================
![](https://gyazo.com/4bdf2b5b1a1690f4ec26052263276df8.png)

## mako について
[ｍako](https://www.makotemplates.org/])は、Pythonで実装されたオープンソースのテンプレートエンジンです。Jinja2がDjango Templateに触発されてその互換性を意識して設計されているのに対して、Makoは高速パフォーマンスを実現するように設計されています。
また、使用方法もかなり簡単で簡単で、ほんの数行のコードでテンプレートをデザインすることができます。 強力で機能豊富なツールであり、優れたドキュメントを備えています。ドキュメントは重要です。
機能的には、フィルター、継承、呼び出し可能ブロック、および組み込みのキャッシュシステムが含まれ、大規模または複雑なWebプロジェクトに適用することができます。

Makoは、RedditがWebページを強化するために使用しているだけでなく、PyramidやPylonsなどのWebフレームワークのデフォルトのテンプレートエンジンです。
データベースマイグレーションツール [alembic](https://alembic.sqlalchemy.org/en/latest/]) でもマイグレーションファイルの生成のために使用されています。

## インストール
mako は次のようにインストールします。

```
 # Linux or Mac
 $ python -m pip install mako

 # Windwos
 $ py -3 -m pip install mako
```

## 使用方法
次のコードは、もっとも単純なmakoの利用例です。

```
 from mako.template import Template
 t = Template('Hello world!')
 print(t.render())
```

テンプレートを作成してレンダリングする最も基本的な方法は、 `Template` クラスを使用することです。`Template`クラスのコンストラクタにテンプレートの文字列を与えてインスタンスを作成し、`render()`メソッドでレンダリングします。


```
 from mako.template import Template
 t = template('Hello, ${name}!')
 print(t.render(name='Jack'))
```

テンプレートでは `${変数名}` を使用することができ、`rednder()` メソッドのキーワード引数として与えることができます。
テンプレートに渡されたパラメータは、Pythonモジュールにコンパイルされます。 このモジュールには、テンプレートの出力を生成する `render_body()` 関数が含まれています。 `render()` メソッドが呼び出されると、Makoはテンプレートの実行環境を確立し、`render_body()` 関数を呼び出して、結果をバッファーに保存し、その文字列の内容を返します。
変数のセットには、 `render_body()` 関数でアクセスできます。

`render()` メソッドを使用すると、Makoは、テンプレートがアクセスできるすべての変数と、出力を保持するためのバッファーを格納するコンテキストオブジェクトを作成できます。  `render_context()` メソッドを使用して、レンダリング用のテンプレートをレンダリングすることにより、自分でコンテキストを作成することもできます。

```
 from mako.template import Template
 from mako.runtime import Context
 from io import StringIO

 t = Template("hello, ${name}!")
 buf = StringIO()
 ctx = Context(buf, name="jack")
 t.render_context(ctx)
 print(buf.getvalue())
```

テンプレートは、 `filename` パラメーターを使用して、ファイルからテンプレートをロードすることもできます。

```
 from mako.template import Template
 t = Template(filename='docs/sample.tpl')
 print(t.render())
```

パフォーマンスを向上させるために、ファイルからロードされたテンプレートは、生成されたモジュールを汎用Pythonモジュールファイル（ `.py` ファイル）としてファイルシステムにキャッシュすることもできます。これは、`module_directory`引数を追加することで実装されます。

```
 from mako.template import Template
 t = Template(filename='docs/sample.tpl ',
              module_directory='/tmp/mako_modules')
 print(t.render())
```

上記のコードがレンダリングされた後、モジュールのソースコードをむ  `/tmp/mako_modules/docs/sample.tpl.py` ファイルが作成されます。
このモジュールファイルは、次に同じパラメータのテンプレートが作成されたときに自動的に再利用されます。

### TemplateLookupを使用する
現在の例は、すべて単一のテンプレートオブジェクトの使用に関するものです。 テンプレート内のコードで他のテンプレートリソースを見つけたい場合は、URIを使用してそれらを見つける方法が必要です。 この要件は、 `TemplateLookup` クラスによって実現されます。 このクラスは、ディレクトリのリストを見つけるためにテンプレートを渡して構築され、キーワードパラメータとして`Template`オブジェクトに渡されます。

```
 from mako.template import Template
 from mako.lookup import TemplateLookup
 lookup = TemplateLookup(directories=['docs'])
 t = Template(' <%include file="header.txt"/> Hello word! ',
              lookup=lookup)
```

この例では、テンプレートにファイル名 `header.txt` が含まれています。 `header.txt`を見つけるために、`TemplateLookup`クラスのコンストラクトに`directories`引数にファイルを検索するディレクトリをリストで与えてインスタンスオブジェクト`lookup`を生成します。
 `Template` クラスのコンストラクタで、引数`lookup`に`lookup`オブジェクトを与えます。
通常、アプリケーションはほとんどのテンプレートをテキストファイルの形式でファイルシステムに保存します。 実際のアプリケーションは、 `TemplateLookup` オブジェクトの`get_template()`メソッドを使用して直接テンプレートを取得することができます。このメソッドは、必要なテンプレートのURIを引数として受け入れます。

```
 from mako.template import Template
 from mako.lookup import TemplateLookup

 lookup = TemplateLookup(directories=['docs'],
                         module_directory='/tmp/mako_modules')

 def serve_template(t_name, **kwargs):
     t = lookup.get_template(t_name)
     print(t.render(**kwargs)
```

この例では、ディレクトリ `docs` からテンプレートを検索し、すべてのモジュールファイルをディレクトリ`/tmp/ mako_modules`に保存する`templatelookup`のインスタンスを作成します。 URIを`passing/etc/beans/info.txt` などの各ルックアップディレクトリにアタッチしてテンプレートを検索すると、`file/docs/etc/beans/info.txt` が検索され、見つからない場合は`Toplevelnotfound`例外が発生します。
テンプレートがパースされると、 `get_template()` 呼び出しに渡されます。`TemplateLookup`クラスのURIアトリビュートが使用されて、 モジュールファイルの名前を取得します。
上記の例では `/etc/beans/info.txt` によってモジュールファイル`/tmp/mako_modules/etc/beans/info.txt.py`が作成されます。

### キャッシュするテンプレート数を設定する

 `TemplateLookup` は、メモリにキャッシュされたテンプレートの総数を固定値で保持しています。デフォルトのは無制限です。 `collection_size`引数を使用してこの固定値を指定できます。

```
 lookup = TemplateLookup(directories=['/docs '),
                         module_directory='/tmp/mako_modules ',
                         collection_size=500)
```

テンプレートをメモリにロードするための上限は500です。[LRUポリシー](https://ja.wikipedia.org/wiki/ページ置換アルゴリズム])を使用して置換テンプレートをクリーンアップします。
>補足説明：LRUポリシー
>LRU(Least Recently Used)ポリシーは、広さの限られた一時的な保管場所が満杯になったときに、
> 何を棄てるか決定する基準の一つで、最も過去に使用されたものから順に破棄する方式。

### ファイルシステムチェックを設定する

 `TemplateLookup` のもう1つの重要なことは、`filesystem_checks`です。 デフォルトは`True`で、各`get_template()`メソッドは、元のテンプレートファイルの変更時刻とテンプレートの最新の読み込み時刻を比較するテンプレートを返し、ファイルが更新された場合はテンプレートを再読み込みしてコンパイルします。 本番システムでは、`filesystem_checks`を`False`に設定すると、パフォーマンスがいくらか向上する可能性があります。

### Unicodeとエンコーディングの使用

 `Template` および `TemplateLookup` は、`output_encoding` および `encoding_errors` 引数を設定して、出力をPythonでサポートされているエンコード形式に指示することができます。


```
 From mako.template import Template
 from mako.lookup import TemplateLookup

 lookup = TemplateLookup(directories=['docs'],
                         output_encoding='utf-8',
                         encoding_errors='replace')

 t = lookup.get_template ('foo.txt')
 print(t.render ())
```

Python 3では、 `output_encoding` が設定されている場合、`render()`メソッドは`Bytes`オブジェクトまたは文字列を返します。
 `render_unicode()` メソッドはテンプレート出力は文字列になります。

```
 print(t.render_unicode())
```

上記のメソッドには出力エンコードされたパラメーターがなく、単独でエンコードできます。

```
 print(t.render_unicode().encode('utf-8', 'replace'))
```


### 例外の処理
テンプレートの例外は2か所で発生する可能性があります。 1つはテンプレートを見つけて、解析し、コンパイルするとき、もう1つはテンプレートを実行するときです。テンプレートの実行で発生する例外は、通常、問題が発生するPythonコードでスローされます。 Makoには独自の例外クラスのセットがあり、これらは主にテンプレート構造のルックアップおよびコンパイルフェーズで使用されます。 Makoは、mako情報を例外スタックに提供し、例外をテキストまたはHTML形式で出力するためのライブラリルーチンをいくつか提供しています。
Pythonのファイル名、行番号、およびコードフラグメントは、Makoテンプレートのファイル名、行番号、およびコードフラグメントに変換されます。 Makoテンプレートモジュールの行は、元のテンプレートファイルの対応する行に変換されます。

 `text_error_template()` および `html_error_template()` 関数は、例外追跡をフォーマットするために使用されます。
 `sys.exc_info()` を使用して、最後にスローされた例外を取得します。これらのプロセッサの使用法は次のとおりです。


```
 from mako import Exceptions

 try:
     t = lookup.get_template(URI)
     print(t.render())
 except:
     print(Exceptions.text_error_template().render())
```

あるいはエラーメッセージをHTMLで出力する場合は次のようにします。

```
 from Mako import Exceptions

 try:
     t = Lookup.get_template(URI)
     print(t.render ())
 except:
     print(Exceptions.html_error_template().render())
```

 `html_error_template()` テンプレートは、次の2つの引数を受け入れます。
-  `full= False` ：HTMLセクションのみをレンダリングすることを指定
-  `css=False` ：デフォルトのスタイルシートを閉じることを指定

```
 print(Exceptions.html_error_template().render(full=False))
```

 `format_exceptions` フラグを使用して、HTMLレンダリング関数をテンプレートに追加することもできます。 この場合、出力内のテンプレートのレンダリングフェーズでの例外の結果は、`html_error_template()` の出力に置き換えられます。

```
 t = Template(filename='/foo/bar', format_exceptions=True)
 print(t.render())
```

このテンプレートのコンパイルフェーズは、テンプレートが構築され、出力ストリームが定義されていないときに発生することに注意してください。 したがって、ルックアップ、解析、およびコンパイルフェーズの例外は通常処理されませんが、拡散されます。 事前レンダリングトレースにはmako形式の行が含まれていません。つまり、レンダリング前とレンダリング中に発生する例外はさまざまな方法で処理されるため、 `try...except` がより一般的に使用される場合があります。

エラーテンプレート関数で使用される基になるオブジェクトは、 `RichTraceback` オブジェクトです。 このオブジェクトを直接使用して、カスタムエラービューを提供することもできます。 使用例は次のとおりです。


```
 from mako.exceptions import RichTraceback
 try:
     t = lookup.get_template(uri)
     print(t.render())
 except:
     traceback = RichTraceback()
     for (filename, lineno, function, line) in traceback.traceback:
         print(f'File{filename}, line {lineno}, in {function}')
         print(line, '\n')
     print(f'{str(traceback.error.__class__.__name__)}: {traceback.error}')
```

## makoを統合する
### MakoをDjangoに統合する
makoは、Webアプリケーションフレームワークdjangoに統合することができます。
まず、djangomakoモジュールをインストールする必要があります。

```
 $ pip install djangomako
```

Djangoプロジェクトの `settings.py` ファイルで、`middleware_classes` を変更し、`Djangomako.middleware.MakoMiddleware` を追加します。

 settings.py
```
 # ...
 TEMPLATES = [
     # ...
     {
         'BACKEND': 'djangomako.backends.MakoBackend',
         'NAME': 'mako',
         'DIRS': [
             os.path.join(BASE_DIR, 'templates'),
         ],
     },
     # ...
 ]
 # ...
```

DjangoのすべてのシステムテンプレートがMakoテンプレートだと想定されることに注意してください。Django Temaplteをテンプレートバックエンドとして使用する場合は、FBV(Function Base View) で  `using='Django'` を渡すか、CBV(Class Base View) で`template_engine='mako'` を追加します。

 `render_to_response()` 関数を使用して次のことを行います。

```
 from django.shortcuts import render_to_response

 def hello_view (request):
     return render_to_response('Hello.txt', {'name': 'Jack'})
```

### mako を tornado に統合
mako はtornadoで直接使用することができます。使用例は次のとおりです。

```
 import tornado.web
 import mako.lookup
 import mako.template

 LOOKUP = mako.lookup.TemplateLookup(
                             directories=[TEMPLATE_PATH],
                             module_directory='/tmp/mako',
                             output_encoding='utf-8',
                             encoding_errors='replace')

 class BaseHandler(tornado.web.RequestHandler):
     def initialize(self, lookup=LOOK_UP):
         """テンプレートルックアップオブジェクトを設定
            デフォルトは LOOK_UP
         """
         self._lookup = lookup

     def render_string(self, filename, **kwargs):
         """makoテンプレートを使用するために、
            render_stringをオーバーライドする。
            tornado render_stringメソッドと同様に、
            このメソッドもリクエストハンドラー環境を
            テンプレートエンジンに渡します。
         """
         try:
             template = self._lookup.get_template(filename)
             env_kwargs = dict(
                 handler = self,
                 request = self.request,
                 current_user = self.current_user,
                 locale = self.locale,
                 _ = self.locale.translate,
                 static_url = self.static_url,
                 xsrf_form_html = self.xsrf_form_html,
                 reverse_url = self.application.reverse_url,
             )
             env_kwargs.update(kwargs)
             return template.render(**env_kwargs)
         except:
             # exception handler
             pass

     def render(self, filename, **kwargs):
         self.finish(self.render_string(filename, **kwargs))
```

