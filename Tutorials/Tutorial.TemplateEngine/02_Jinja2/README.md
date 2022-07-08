Jinja2を使ってみよう
=================
![](https://gyazo.com/9adfe5855f52e6efdc4957e0598417dc.png)

### Jinja2について
Jinja2はオープンソースで開発されている、人気のあるPythonテンプレートエンジンです。 Django Templateにインスパイアされて開発されましたが、より多用途に適応させることができます。

構成管理ツールのAnsibleやSaltStack、静的サイトジェネレーターPelicanなどのオープンソースアプリケーションは、出力ファイルの生成にJinjaテンプレートエンジンを採用しています。

Jinja2 はテンプレートを読み込んで、そこにデータ与えてレンダリングすることでドキュメントを生成します。

### インストール
拡張モジュールなので次のようにインストールします。

 condaの場合
```
 $ conda install jinja2
```

 pipの場合
```
 # Linux or Mac
 $ python -m  pip install jinja2

 # Windwos
 $ py -3  -m  pip install jinja2
```

### テンプレートとレンダリング
文法などの説明する前に、動作の概要をみてみましょう。
まず、 `name` で与えた文字列を展開する簡単な例です。

```
 In [2]: # %load jinja2_hello.py
    ...: from jinja2 import Template
    ...: template = Template('Hello {{ name }}!')
    ...: template.render(name='Python')
    ...:
 Out[2]: 'Hello Python!'
```

もう少しだけ、複雑にしてみましょう。
まず、 `Template()` に与えるテンプレートファイルを次のように外部に定義します。

 hello.txt
```txt
 Hello {{ name }}!
```

このテンプレートファイルを読み取り、データをレンダリングする処理が次のコードです。

```
 In [2]: # %load jinja2_hello2.py
    ...: from jinja2 import FileSystemLoader, Environment
    ...:
    ...: def render_from_template(directory, template_name, **kwargs):
    ...:     loader = FileSystemLoader(directory)
    ...:     env = Environment(loader=loader)
    ...:     template = env.get_template(template_name)
    ...:     return template.render(**kwargs)
    ...:
    ...: doc = render_from_template('.', 'greeting.txt', name='Freddie')
    ...: print(doc)
    ...:
 Hello Freddie!
```

### Pythonオブジェクトをレンダリング
テンプレートファイルで２重中括弧（ `{{...}}` ) に囲むオブジェクトは、特殊メソッド`__str__()`が有効であれば、文字列オブジェクトに限定されません。

まず、テンプレートファイルを次のようにしてみましょう。

 artist.html
```html
 <html>
  <body>
   <h1>{{ artist.firstname }} {{ artist.lastname }}:</h1>
   <p>Born: {{ artist.born_place }}
      Birthday: {{ artist.born_date }}
  </body>
 </html>
```

これをレンダリングするコードは次のようになります。

```
 In [2]: # %load jinja2_artist.py
    ...: from jinja2 import FileSystemLoader, Environment
    ...:
    ...: def render_from_template(directory, template_name, **kwargs):
    ...:     loader = FileSystemLoader(directory)
    ...:     env = Environment(loader=loader)
    ...:     template = env.get_template(template_name)
    ...:     return template.render(kwargs)
    ...:
    ...: class Artist:
    ...:     pass
    ...:
    ...: artist = Artist()
    ...: artist.firstname = 'Freddie'
    ...: artist.Lastname = 'Mercury'
    ...: artist.born_place = 'Farrokh Bulsara'
    ...: artist.born_date = '1946-9-5'
    ...:
    ...: doc = render_from_template('.', 'artist.html', artist=artist)
    ...: print(doc)
    ...:
 <html>
  <body>
   <h1>Freddie :</h1>
   <p>Born: Farrokh Bulsara
      Birthday: 1946-9-5
  </body>
 </html>

```

ドット表記法（ `.` )は、辞書型オブジェクトやイテラブルオブジェクトのマジックメソッド`__getattr__()`または`__getitem__()`をサポートしているオブジェクトで利用できます。

 `{{ ... }}` でレンダリングさせるオブジェクトの記述方法には２つの方法があります。

- ドット表記法（ `.` )：　 `{{ artist.firstname }}`
- 辞書キーワード指定：  `{{ artist['firstname'] }}`


### デリミタ
これまでにも説明してきているように、テンプレートにはJinja2がレンダリングを制御するための**デリミタ(Delimiter)** が記述されています。

-  `{%....%}` ：Jinja2の制御文を記述
-  `{{....}}` ：指定したオブジェクトがレンダリングされて出力される
-  `{#....#}` ：コメント。内容はレンダリングされない。
-  `#....##` Pythonの式を記述、複数行もOK

### 条件判断でレンダリング
 `name` が与えられていないときは、`Hello Python!`と出力するように、
テンプレートファイル側で条件判断をさせてみましょう。

 greeting.txt
```txt
 {% if name != ''%}
 Hello {{ name }}!
 {% else %}
 Hello Python!
 {% endif %}
```

これをレンダリングするコードは `jinja2_hello2.py` とほぼ同じものです。

```
 In [2]: # %load jinja2_greeting.py
    ...: from jinja2 import FileSystemLoader, Environment
    ...:
    ...: def render_from_template(directory, template_name, **kwargs):
    ...:     loader = FileSystemLoader(directory)
    ...:     env = Environment(loader=loader)
    ...:     template = env.get_template(template_name)
    ...:     return template.render(**kwargs)
    ...:
    ...: doc = render_from_template('.', 'greeting.txt', name='')
    ...: print(doc)
    ...:

 Hello Python!
```

この例のレンプレートファイルで使用しているJinja2の機能は次のものです。

-  `{% ... %}` ：表記の中にレンダリングする操作を記述する
-  `{% if 条件式 %} ... {% endif %}` ：`if`文の構文


### ループ処理
生成するドキュメントにテーブルがあるようなとき、リストオブジェクト内容をそのままテンプレートに渡して、テンプレートファイル側でループ処理できれば、コードが簡単になるはずです。

 artist_list.html
```html
 <html>
  <body>
   <h1>Artist Birthday(Artist: {{ artist_list|length }})</h1>
   <table>
     <tr><td> Name </td>
         <td> Birthday </td>
         <td> Born place </td>
     </tr>
     {% for artist in artist_list %}
      <tr>
        <td> {{ artist.firstname }} {{ artist.lastname }} </td>
        <td> {{ artist.born_date }} </td>
        <td> {{ artist.born_place }} </td>
      </tr>
     {% endfor %}
     </table>
  </body>
 </html>
```

これをレンダリングするコードの例です。

 jinja2_artist_list.py
```
 from jinja2 import FileSystemLoader, Environment

 def render_from_template(directory, template_name, **kwargs):
     loader = FileSystemLoader(directory)
     env = Environment(loader=loader)
     template = env.get_template(template_name)
     return template.render(kwargs)

 artist_list=[
     {
         'firstname': 'Freddie',
         'lastname': 'Mercury',
         'born_place': 'Farrokh Bulsara',
         'born_date': '1946-9-5'
     },
     {
         'firstname': 'David',
         'lastname': 'Bowie',
         'born_place': 'Brixton, London, England',
         'born_date': '1947-1-8'
     },
 ]
 doc = render_from_template('.', 'artist_list.html',
                            artist_list=artist_list)
 print(doc)
```

```
 In [1]: %run jinja2_artist_list.py
 <html>
  <body>
   <h1>Artist Birthday (Artist: 2)</h1>
   <table>
     <tr><td> Name </td>
         <td> Birthday </td>
         <td> Born place </td>
     </tr>

      <tr>
        <td> Freddie Mercury </td>
        <td> 1946-9-5 </td>
        <td> Farrokh Bulsara </td>
      </tr>

      <tr>
        <td> David Bowie </td>
        <td> 1947-1-8 </td>
        <td> Brixton, London, England </td>
      </tr>

     </table>
  </body>
 </html>
```

レンダリングするコードの中にループ処理がないことに注目してください。
この例のテンプレートファイルで使用しているJinja2の機能は次のものです。

-  `{% for val in interableObject %} ... {% endfor %}` ：繰り返し処理
-  `{{ object| filter }}` ： オブジェクトがフィルタで処理されてレンダリング

この例で使用しているフィルタ  `length` はオブジェクトの長さを返すものです。
他にも多数のフィルタが提供されています。

### フィルタ
jinja2にはたくさんのフィルタがあります。一例をあげておきます。

-  `default` ：`{{ my_variable|default('my_variable is not defined') }}`
-  `max` : `{{ [1, 2, 3]|max }}`  → 3
-  `min` : `{{ [1, 2, 3]|min }}`  → 1
-  `length` : `{{ [1, 2, 3]|length }}`  → 3
-  `replace` : `{{ "Hello World"|replace("World", "Python") }}` → Hello Python
-  `upper` : `{{ "Hello World"|upper }}` → HELLO WORLD
-  `lower` ：`{{ "Hello World"|lower }}` → hello world
-  `select` ： `{{ "Hello World"|select("equalto", "World") }}` → World
-  `join` ： `{{ "Hello World" | join("|") }}` → Hello|World

### 独自フィルタ
独自にフィルタを定義することもできます。
次のコード、文字列の１文字を重複させる `double` というフィルタを定義する例です。

```
 In [2]: # %load jinja2_customfilter.py
    ...: from jinja2 import FileSystemLoader, Environment
    ...:
    ...: def double(arg):
    ...:     data=''
    ...:     for s in list(str(arg)):
    ...:         data += s*2
    ...:     return data
    ...:
    ...: def render_from_template(directory, template_name, **kwargs):
    ...:     loader = FileSystemLoader(directory)
    ...:     env = Environment(loader=loader)
    ...:     env.filters['double'] = double
    ...:     template = env.get_template(template_name)
    ...:     return template.render(kwargs)
    ...:
    ...: items=['Osaka', 'Python']
    ...:
    ...: doc = render_from_template('.', 'custom_filter.html', items=items)
    ...: print(doc)
    ...:
 <html>
  <body>
   <h1>Jinja2 filter examples</h1>
   <table>
     <h2> my custom filer: duble </h2>

      <p> OOssaakkaa

      <p> PPyytthhoonn

     </table>
  </body>
 </html>
```

 custom_filter.html
```html
 <html>
  <body>
   <h1>Jinja2 filter examples</h1>
   <table>
     <h2> my custom filer: duble </h2>
     {% for item in items %}
      <p> {{ item | double }}
     {% endfor %}
     </table>
  </body>
 </html>
```


### テンプレートの継承
Jinja2 が強力な機能のひとつにテンプレートの継承があります。
これが有用になる場面を考えてみましょう。例えば、Webアプリケーションでサイト全体のCSSファイルを設定しておき、個別には各ページは差分を定義することができれば、コードばかりでなくテンプレートも簡潔に記述することができるようになるはずです。

まず、ヘッダ情報のためのテンプレートファイルを用意します。

 header.html
```html
 <HEAD>
   <TITLE>{{ title }}</TITLE>
 </HEAD>
```

既存のテンプレートファイルを取り込むためには、次のようにします。

 base.html
```html
 <HTML>
     {% include 'header.html' %}
   <BODY>
   </BODY>
 </HTML>
```

このテンプレートファイルは次のようにレンダリングできます。

```
 In [2]: # %load jinja2_template_inheritance1.py
    ...: from jinja2 import FileSystemLoader, Environment
    ...:
    ...: def render_from_template(directory, template_name, **kwargs):
    ...:     loader = FileSystemLoader(directory)
    ...:     env = Environment(loader=loader)
    ...:     template = env.get_template(template_name)
    ...:     return template.render(**kwargs)
    ...:
    ...: doc = render_from_template('.', 'base.html',
    ...:                                  title='This is sample Page')
    ...: print(doc)
    ...:
 <HTML>
     <HEAD>
   <TITLE>This is sample Page</TITLE>
 </HEAD>
   <BODY>
   </BODY>
 </HTML>
```

次に、この `base.html` を`block` を取り込むように修正してみます。

 base_with_block.html
```html
 <HTML>
     {% include 'header.html' %}
   <BODY>
     {% block content %}
     {% endblock %}
   </BODY>
 </HTML>
```

 `base_with_block.html` テンプレートからチャイルド・テンプレートを作ります。

 child.html
```html
 {% extends "base_with_block.html" %}

 {% block content %}
   <p>
   {{ body }}
   </p>
 {% endblock %}
```

これをレンダリングしてみましょう。


```
 In [2]: # %load jinja2_template_inheritance2.py
    ...: from jinja2 import FileSystemLoader, Environment
    ...:
    ...: def render_from_template(directory, template_name, **kwargs):
    ...:     loader = FileSystemLoader(directory)
    ...:     env = Environment(loader=loader)
    ...:     template = env.get_template(template_name)
    ...:     return template.render(**kwargs)
    ...:
    ...: doc = render_from_template('.', 'child.html',
    ...:                            title='This is sample Page',
    ...:                            body='Hello Python!')
    ...: print(doc)
    ...:
 <HTML>
     <HEAD>
   <TITLE>This is sample Page</TITLE>
 </HEAD>
   <BODY>

   <p>
   Hello Python!
   </p>

   </BODY>
 </HTML>
```

ベース・テンプレートで  `{% block ブロック名 %}` として記述したものは、
実際にはチャイルド・テンプレートで定義されるものです。
ブロック名は任意の文字列で構いません。（例： `{% block footer %}` など）

### テンプレートエンジンの効用
テンプレートエンジンを使用すると、デザインとコントロール(制御)を分離することができるようになります。例えばWebアプリケーションでは、プログラマとデザイナーが並行して作業をすすめるといったような開発を行うことができるというわけです。

参考:
- [Jinja オフィシャル](https://palletsprojects.com/p/jinja/])
- TTL255 - Przemek Rogala's Blog - [Jinja2 Tutorial Series](https://ttl255.com/jinja2-tutorial-part-1-introduction-and-variable-substitution/])
