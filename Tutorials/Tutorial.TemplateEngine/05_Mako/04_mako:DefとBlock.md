mako:DefとBlock
=================
![](https://gyazo.com/4bdf2b5b1a1690f4ec26052263276df8.png)

## def と block
 `<%def>` と`<%block>` は、テキストやコードのブロックを区切る2つのタグです。 これらは両方とも、生成されたPython内に呼び出し可能な関数、つまりPython の `def`文として存在します。 それらは、スコープと呼び出し方法が異なります。 `<%def>`は名前付けすることができ、Python の`def`文に非常によく似た構造を提供します。これに対して、`<%block>`はよりレイアウトを重視した構造を提供します。

### defの使用
 `<%def>` タグには `name` アトリビュートが必要です。

```
 <%def name="hello()">
     hello world
 </%def>
```

 `<%def>` を呼び出すために、通常は式として呼び出されます。

```
 the def:  ${hello()}
```

 `<%def>` が別の `<%def>` 内にネストされていない場合、それは**トップレベルのDef** と呼ばれ、定義された場所を含め、テンプレート内のどこからでもアクセスできます。

すべての定義は、トップレベルかどうかに関係なく、含まれているテンプレートとまったく同じ方法で現在のコンテキスト名前空間にアクセスできます。
次のテンプレートが、コンテキスト内の変数  `username` と `accountdata` を使用して実行されたとします。

```
 Hello there ${username}, how are ya.  Lets see what your account says:

 ${account()}

 <%def name="account()">
     Account for ${username}:<br/>

     % for row in accountdata:
         Value: ${row}<br/>
     % endfor
 </%def>
```

 `username` 変数と `accountdata` 変数は、メインテンプレート本体と `name` アトリビュートに `account()` を持つ `<%def>` の本体にあります。

 `<%def>` は単なるPython関数であるため、引数を定義して渡すこともできます。

```
 ${account(accountname='john')}

 <%def name="account(accountname, type='regular')">
     account name: ${accountname}, type: ${type}
 </%def>
```

 `<%def>` の引数を宣言するときは、通常のPythonの規則に従う必要があります（つまり、デフォルト値のキーワード引数を除くすべての引数が必要です）。 これは、存在しない名前を参照した場合に `UNDEFINED` と評価されるコンテキストレベルの変数を使用するのとは対照的です。

#### 他のファイルからのDefの呼び出し
トップレベルのDefはテンプレートのモジュールによってエクスポートされ、外部から呼び出すことができます。 他のテンプレートや通常のPythonコードからのものを含みます。 別のテンプレートから `<%def>` を呼び出すことは、 `<%include>` を使用するようなものです。ただし、テンプレート全体ではなく、テンプレート内の特定の関数を呼び出す点が異なります。

リモートの `<%def>` 呼び出しも、Pythonの他のモジュールから関数を呼び出すのと少し似ています。 別のテンプレートからインポートするステップがあります。 その後、1つまたは複数の関数が使用可能になります。

別のテンプレートをインポートするには、 `<%namespace>` タグを使用します。

```
 <%namespace name="mystuff" file="mystuff.html"/>
```

上記のタグは、ローカル変数 `mystuff` を現在のスコープに追加します。

次に、 `mystuff` からDefを呼び出します。

```
 ${mystuff.somedef(x=5,y=7)}
```

 `<%namespace>` タグは、ローカル変数スペースに名前をプルしたり、`import` アトリビュートを使用してすべての名前を表すためにアスタリスク記号( `*` )を使用したりするなど、Pythonの `import` 文の使用方法と同じ方法をサポートしています。

```
 <%namespace file="mystuff.html" import="foo, bar"/>
```

これは、名前空間の概念の簡単な紹介です。名前空間は、これらのドキュメントに独自の章があるMakoの中心的な概念です。 詳細と例については、名前空間を参照してください。

### プログラムでDefを呼び出す
 `DefTemplate` オブジェクトを返す `Template.get_def()` メソッドを使用して、任意の `Template` オブジェクトからプログラムでDefを呼び出すことができます。 これは、親テンプレートが作成するテンプレートサブクラスであり、他のテンプレートと同じように使用できます。

```
 from mako.template import Template

 template = Template("""
     <%def name="hi(name)">
         hi ${name}!
     </%def>

     <%def name="bye(name)">
         bye ${name}!
     </%def>
 """)

 print(template.get_def("hi").render(name="ed"))
 print(template.get_def("bye").render(name="ed"))
```

### Defのネスト
Defモデルは、クロージャーに関する通常のPythonルールに従います。 別の `<%def>` 内で `<%def>` を宣言すると、外側（親）が囲んでいるスコープ内で宣言されます。

```
 <%def name="mydef()">
     <%def name="subdef()">
         a sub def
     </%def>

     i'm the def, and the subcomponent is ${subdef()}
 </%def>
```

Pythonと同様に、内側の `<%def>` の外側に存在する名前もPythonの内部に存在します。

```
 <%
     x = 12
 %>
 <%def name="outer()">
     <%
         y = 15
     %>
     <%def name="inner()">
         inner, x is ${x}, y is ${y}
     </%def>

     outer, x is ${x}, y is ${y}
 </%def>
```

Def内の名前に割り当てると、その名前はそのDefのスコープに対してローカルであると宣言されます（これもPythonの `self` のように）。 これは、次のコードでエラーが発生することを意味します。

```
 <%
     x = 10
 %>
 <%def name="somedef()">
     ## error !
     somedef, x is ${x}
     <%
         x = 27
     %>
 </%def>
```

 `x` への割り当ては、`x` を somedef のスコープに対してローカルとして宣言し、それをレンダリングしようとする式で「外側」バージョンに到達できないようにするためです。

### 埋め込みコンテンツやその他のDefを使用してDefを呼び出す
Def内のDefの裏側は、コンテンツを使用したDef呼び出しです。ここでDefを呼び出し、同時に、呼び出されるDefで使用できるコンテンツのブロック（または複数のブロック）を宣言します。このような呼び出しの主なポイントは、他のテンプレート言語のカスタムタグ作成システムと同じように、カスタムのネスト可能なタグを作成することです。外部タグは、ネストされたタグの実行を制御し、状態をそれらに伝達できます。 Makoを使用する場合のみ、外部Pythonモジュールを使用する必要はなく、テンプレート内で任意にネスト可能なタグを定義できます。

これを実現するために、ターゲットDefは、通常の `${...}` 構文の代わりに `<%namespacename:defname>` の形式を使用して呼び出されます。 機能的には `<%call>` タグと同等であり、`<%call expr='namespacename.defname(args)'>` の形式を取ります。  `<%call>` タグはMakoのすべてのバージョンで使用できますが、Mako 0.2.3で導入された新しいスタイルの方が見慣れているかもしれません。呼び出しの名前空間部分は、Defが定義されている名前空間の名前です。最も単純なケースでは、これはローカルまたは`self`であり、現在のテンプレートの名前空間を参照できます。
ターゲットDefが呼び出されると、変数呼び出し元は、呼び出し元によって定義された本体と他の定義を含む別の名前空間を含むコンテキストに配置されます。本体自体は `body()` メソッドによって参照されます。
次の例は、 `caller.body()` を操作してカスタムタグの本体を呼び出す `<%def>` を作成します。

```
 <%def name="buildtable()">
     <table>
         <tr><td>
             ${caller.body()}
         </td></tr>
     </table>
 </%def>

 <%self:buildtable>
     I am the table body.
 </%self:buildtable>
```

これにより、出力（空白形式）が生成されます。

```
 <table>
     <tr><td>
         I am the table body.
     </td></tr>
 </table>
```

古い `<%call>` タグを使用すると、次のようになります。

```
 <%def name="buildtable()">
     <table>
         <tr><td>
             ${caller.body()}
         </td></tr>
     </table>
 </%def>

 <%call expr="buildtable()">
     I am the table body.
 </%call>
```

 `body()` は、複数回実行することも、まったく実行しないこともできます。 これは、def-call-with-contentを使用して、イテレータ、条件などを構築できることを意味します。

```
 <%def name="lister(count)">
     % for x in range(count):
         ${caller.body()}
     % endfor
 </%def>

 <%self:lister count="${3}">
     hi
 </%self:lister>
```

これは次のような出力になります。

```
 hi
 hi
 hi
```

上記では、3をPython式として渡すため、整数のままであることに注意してください。

カスタムの `conditional` タグの例：

```
 <%def name="conditional(expression)">
     % if expression:
         ${caller.body()}
     % endif
 </%def>

 <%self:conditional expression="${4==4}">
     i'm the result
 </%self:conditional>
```

これは次のような出力になります。

```
 i'm the result
```

それだけではありません。  `body()` 関数は引数を処理することもできます。これにより、呼び出し可能なbodyのローカル名前空間が拡張されます。 呼び出し元は、引数名のコンマ区切りリストである`args`アトリビュートを使用して、ターゲットDefから受け取ると予想される引数を定義する必要があります。 以下では、`<%def>` が呼び出し元の `body()` を呼び出し、引数からデータの要素を渡します。

```
 <%def name="layoutdata(somedata)">
     <table>
     % for item in somedata:
         <tr>
         % for col in item:
             <td>${caller.body(col=col)}</td>
         % endfor
         </tr>
     % endfor
     </table>
 </%def>

 <%self:layoutdata somedata="${[[1,2,3],[4,5,6],[7,8,9]]}" args="col">\
 Body data: ${col}\
 </%self:layoutdata>
```

これは次のような出力になります。

```
 <table>
     <tr>
         <td>Body data: 1</td>
         <td>Body data: 2</td>
         <td>Body data: 3</td>
     </tr>
     <tr>
         <td>Body data: 4</td>
         <td>Body data: 5</td>
         <td>Body data: 6</td>
     </tr>
     <tr>
         <td>Body data: 7</td>
         <td>Body data: 8</td>
         <td>Body data: 9</td>
     </tr>
 </table>
```

 `body()` 関数だけを呼び出すことに固執する必要はありません。 呼び出し元は任意の数の呼び出し可能オブジェクトを定義できるため、`<%call>`タグでレイアウト全体を生成できます。

```
 <%def name="layout()">
     ## layoutの定義
     <div class="mainlayout">
         <div class="header">
             ${caller.header()}
         </div>

         <div class="sidebar">
             ${caller.sidebar()}
         </div>

         <div class="content">
             ${caller.body()}
         </div>
     </div>
 </%def>

 ## layoutを呼び出す
 <%self:layout>
     <%def name="header()">
         I am the header
     </%def>
     <%def name="sidebar()">
         <ul>
             <li>sidebar 1</li>
             <li>sidebar 2</li>
         </ul>
     </%def>

         this is the body
 </%self:layout>
```

これは次のような出力になります。

```
 <div class="mainlayout">
     <div class="header">
     I am the header
     </div>

     <div class="sidebar">
     <ul>
         <li>sidebar 1</li>
         <li>sidebar 2</li>
     </ul>
     </div>

     <div class="content">
     this is the body
     </div>
 </div>
```

 `<%call>` または`<%namespacename:defname>` 呼び出し構文で実行できることの数は膨大です。 囲んでいる`<form>`タグやネストされたHTML入力要素などのフォームウィジェットライブラリ、または`<div>`やその他の要素を使用したポータブルラッピングスキームを作成できます。 データベースなどからのデータの行を解釈するタグを作成して、各行の個々の列を、任意の方法で行をレイアウトする`body()`呼び出し可能オブジェクトに提供できます。 基本的に、他のシステムの「カスタムタグ」またはタグライブラリで行うことはすべて、Makoは`<%def>`タグと、`<%namespacename:defname>`または`<%call>`を介して呼び出されるプレーンなPython呼び出し可能オブジェクトを提供します。

### ブロックの使用
 `<%block>` タグは、`<%def>`タグにいくつかの新しい工夫を加え、レイアウトに合わせてより厳密に調整できるようにします。
ブロックの例：

```
 <html>
     <body>
         <%block>
             this is a block.
         </%block>
     </body>
 </html>
```

上記の例では、単純なブロックを定義します。 ブロックは、定義された場所にコンテンツをレンダリングします。 ブロックは私たちのために呼び出されるので、名前は必要ありません。上記は匿名ブロックと呼ばれます。 したがって、上記のテンプレートの出力は次のようになります。

 html
```
 <html>
     <body>
             this is a block.
     </body>
 </html>
```

したがって、実際には、上記のブロックはまったく効果がありません。 その有用性は、修飾子の使用を開始するときに得られます。 たとえば、ブロックにフィルターを適用することができます。

```
 <html>
     <body>
         <%block filter="h">
             <html>this is some escaped html.</html>
         </%block>
     </body>
 </html>
```

またはおそらくキャッシュディレクティブ：

```
 <html>
     <body>
         <%block cached="True" cache_timeout="60">
             このコンテンツは60秒間キャッシュされる
         </%block>
     </body>
 </html>
```

ブロックは、Defと同じように、反復、条件付きでも機能します。

```
 % if some_condition:
     <%block>condition is met</%block>
 % endif
```


ブロックはテンプレートで定義された時点でレンダリングされますが、基になる関数は生成されたPythonコードに1回だけ存在するため、ループ内などにブロックを配置しても問題はありません。 無名ブロックはローカルレンダリング本体のクロージャとして定義されているため、ローカル変数スコープにアクセスできます。

```
 % for i in range(1, 4):
     <%block>i is ${i}</%block>
 % endfor
```

### 名前付きブロックの使用
ブロックが便利なところはブロックに名前を付けることができることです。名前付きブロックは、継承テンプレートによってオーバーライドできるレイアウトの領域を定義するという点で、Jinja2のブロックタグにいくらか似せて動作するように調整されています。  `<%def>` タグとは対照的に、ブロックに付けられた名前は、ネストの深さに関係なく、テンプレート全体でグローバルです。

```
 <html>
 <%block name="header">
     <head>
         <title>
             <%block name="title">Title</%block>
         </title>
     </head>
 </%block>
 <body>
     ${next.body()}
 </body>
 </html>
```

このの例には、 `header` と i`title` という2つの名前付きブロックがあり、どちらも継承テンプレートから参照できます。 この使用法の詳細なウォークスルーは、継承にあります。

上記の名前付きブロックには、Defのように引数宣言がないことに注意してください。 ただし、Python関数として実装されているため、最初の定義を超えてさらに何度も呼び出すことができます。

```
 <div name="page">
     <%block name="pagecontrol">
         <a href="">previous page</a> |
         <a href="">next page</a>
     </%block>

     <table>
         ## some content
     </table>

     ${pagecontrol()}
 </div>
```

この `pagecontrol` によって参照されるコンテンツは、`<table>` タグの上と下の両方にレンダリングされます。

健全性に保つために、名前付きブロックには、Defにはない制限があります。

-  `<%block>` 宣言に引数の署名を含めることはできない
-  `<%block>` の名前は、テンプレートで重複して定義できない
ネストに関係なく、同じ名前の2つのブロックが1つのテンプレートのどこかにある場合はエラーが発生します。トップレベルのDefがブロックの名前と同じ名前を共有している場合、同様のエラーが発生します。
- 名前付きブロックは、Def内、または「呼び出し」の本体内で定義できない
つまり `<%call>` または `<%namespacename:defname>` タグ内で定義することはできません。
ただし、無名ブロックは可能です。

### 名前付きブロックでのページ引数の使用
名前付きブロックは、トップレベルの定義に非常によく似ています。  `<%page>` タグを介してテンプレートに渡された引数が自動的に使用できないという点で、これらのタイプの定義と同様の制限があります。 `<%page>` タグでの引数の使用については、 `body()` メソッドのセクションで説明し、引数を渡す継承されたテンプレートからテンプレートの `body()` メソッドが呼び出された場合や、テンプレートがから呼び出された場合などのシナリオを指します。引数付きの `<%include>` タグ。名前付きブロックがページに渡された同じ引数を共有できるようにするには、`args` アトリビュートを使用できます。

```
 <%page args="post"/>

 <a name="${post.title}" />

 <span class="post_prose">
     <%block name="post_prose" args="post">
         ${post.content}
     </%block>
 </span>
```

この例の場合、テンプレートが `<%include file="post.mako" args="post=post"/>` のようなディレクティブを介して呼び出されると、`post` 変数は本体と `post_prose` ブロックの両方で使用できます。

同様に、 `**pageargs` 変数は、 `<%page>` タグで明示されていない引数に対して、名前付きブロックにのみ存在します。

```
 <%block name="post_prose">
     ${pageargs['post'].content}
 </%block>
```

 `args` 属性は、名前付きブロックでのみ許可されます。 無名ブロックを使用すると、Python関数は常に呼び出し自体と同じスコープでレンダリングされるため、無名ブロックの外部で直接使用できるものはすべて内部でも使用できます。


