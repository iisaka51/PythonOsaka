mako:テンプレートの継承
=================
![](https://gyazo.com/4bdf2b5b1a1690f4ec26052263276df8.png)


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

1.  `index.html` がレンダリングされると、制御はすぐに `base.html` に移ります。
2. 次に、 `base.html` はHTMLドキュメントの上部をレンダリングしてから、
 `<%block name="header">` ブロックを呼び出します。これは、`self.header()` 関数を呼び出します。 `index.html` は最上位のテンプレートであり、ヘッダーと呼ばれるブロックも定義しているため、`base.html` に存在するものではなく、最終的に実行されるのはこのヘッダーブロックです。
3. コントロールは `base.html` に戻ります。さらにいくつかのHTMLがレンダリングされます。
4.  `base.html` は `self.body()` を実行します。すべてのテンプレートベースの名前空間の `body()` 関数は、テンプレートの本体を参照するため、`index.html` の本体がレンダリングされます。
5.  `self.body()` 呼び出し中に `index.html` で `<%block name="header">` が検出されると、条件がチェックされます。現在継承されているテンプレート、つまり `base.html` もこのブロックを定義している場合、 `<%block>` はここでは実行されません。継承メカニズムは、親テンプレートがこのブロックのレンダリングを担当していることを認識しています（実際にはすでに実行されています）。言い換えると、ブロックはその最下部のスコープでのみレンダリングされます。
6. コントロールは `base.html` に戻ります。より多くのHTMLがレンダリングされた後、
 `<%block name="footer">` 式が呼び出されます。
7. フッターブロックは `base.html` でのみ定義されているため、フッターの最上位の定義であり、実行されます。  `index.html` でもフッターが指定されている場合、そのバージョンはベースのバージョンをオーバーライドします。
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

ヘッダーを上書きするときに、独自のヘッダーブロックに加えて、親のヘッダーブロックを呼び出すために、追加の呼び出し `${parent.heade()}` を追加したことに注意してください。

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

上記の場合、継承テンプレートは `<%block name="title">` を1回だけ定義でき、 `<title>` セクションと `<h2>` の両方のベーステンプレートで使用されます。

### Defs ではどう記述するのか
前述の例では、 `<%block>` タグを使用して、オーバーライドするコンテンツの領域を生成しました。 Mako 0.4.1より前のバージョンでは、`<%def>`タ グを利用していました。結局のところ、名前付きブロックと `<%def>` タグはほとんど同じです。 `def`は単にそれ自体を自動的に呼び出さず、より柔軟でPythonの`self`に似て、より自由な名前付けとスコープのルールを持っていますが、レイアウトにはあまり適していません。
 `<%def>` タグで記述すると次のようになります。

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

上記では、定義と呼び出しが一度にではなく2つの別々の場所で定義されるという点で、 `<%def>` が `<%block>` とは異なることを示しています。 2つを組み合わせると、 `<%block>` とほぼ同じように実行できます。

```
 <div class="header">
     <%def name="header()"></%def>${self.header()}
 </div>
```

この種の使用法では、 `<%block>` は明らかに `<%def>` よりも合理化されています。 さらに、`<%def>` を使用した上記のインラインアプローチは、ネストでは機能しません。

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

この場合、 `<%def name="title()">` は、Def内のDefであるため、テンプレートのエクスポートされた名前空間の一部ではなく、`self` の一部にもなりません。 継承されたテンプレートがトップレベルで独自のタイトル定義を定義した場合、それは呼び出されますが、上記の「デフォルトのタイトル」は、何があっても自分自身にはまったく存在しません。 これが期待どおりに機能するためには、代わりに次のように言う必要があります。

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

したがって、 `<%block>` タグは、ネストされたブロックが外部で使用できないという制限を解除しますが、これを実現するには、単一のテンプレート内のすべてのブロック名がテンプレート内でグローバルに一意である必要があるという制限を追加します。 `<%block>` を `<%def>` 内で定義することはできません。これは、`<%def>` よりも具体的なユースケースに適した、より制限されたタグです。

### 次の名前空間を使用してコンテンツラッピングを生成
3つ以上のテンプレートにまたがる継承チェーンがある場合があります。または、そうではないかもしれませんが、追加の継承されたテンプレートをチェーンの途中に挿入してスムーズに統合できるようにシステムを構築したいと考えています。各テンプレートが本体内でのみレイアウトを定義する場合は、 `self.body()` を呼び出して、継承するテンプレートの本体を取得することはできません。これは、最上位の本体にすぎないためです。次のテンプレートの本体を取得するには、名前空間`next`を呼び出します。これは、現在のテンプレートの直後にあるテンプレートの名前空間です。

 `self.body()` を呼び出す `base.html` の行を、代わりに `next.body()` を呼び出すように変更しましょう。

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

また、 `base.html` から継承する `layout.html` という中間テンプレートを追加しましょう。

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

そして最後に、代わりに `layout.html` から継承するように `index.html` を変更します。
 html
```
 ## index.html
 <%inherit file="layout.html"/>

 ## .. rest of template
```

この設定では、 `next.body()` を呼び出すたびに、継承チェーン内の次のテンプレートの本体がレンダリングされます（base.html-> layout.html-> index.htmlと記述できます）。 制御は引き続き最初に最下部のテンプレートbase.htmlに渡され、selfは特定の定義の最上位の定義を参照します。

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

この例のように、 `base.html` の `<html>`、`<body>`、ヘッダー/フッターのレイアウト、`layout.html`の `<ul>` と `mainlayout`セクション、`index.html`の本体とそのオーバーライドがあります。 ヘッダー定義 `layout.html`テンプレートは、`base.html`が何も変更することなく、チェーンの中央に挿入されます。 次の名前空間がないと、`index.html`の本体しか使用できませんでした。 `layout.html`の本文コンテンツを呼び出す方法はありません。

### 親の名前空間を使用して定義を拡張
次に呼び出される親の反対である、他の継承固有の名前空間を見てみましょう。  `parent` は、現在のテンプレートの直前にあるテンプレートの名前空間です。 この名前空間の便利な点は、Defまたはブロックがオーバーライドされたバージョンを呼び出せることです。 これは思ったほど難しくはなく、Pythonでクラス継承したときの `super()` を使用するのと非常によく似ています。 `index.html` を変更して、 `layout.html` のツールバー関数によって提供される選択のリストを拡張しましょう。

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

この例では、継承されたテンプレート `layout.html` 内のツールバーの定義をオーバーライドすることを目的とした `toolbar()` 関数を実装しました。 ただし、`layout.html` のコンテンツも必要なので、コンテンツが必要なときはいつでも、この場合は独自の選択を追加する前に、親名前空間を介して呼び出します。 したがって、全体の出力は次のようになります。

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

### テンプレートの継承で<%include>を使用
混乱の一般的な原因は、 `<%include>` タグの動作であり、多くの場合、テンプレート継承内での相互作用と関連しています。 `<%include>`タグを理解するための鍵は、それが動的であるということです。ランタイム、インクルード、静的インクルードではありません。 `<%include>`は、テンプレートのレンダリング時にのみ処理され、継承のセットアップ時には処理されません。参照されるテンプレートは、現在の継承構造にリンクされていない完全に別個のテンプレートとして完全に実行されます。

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

上記では、 `partials.mako` のインクルードを介して`parent.mako`に存在する同じブロックをオーバーライドした結果として、`child.mako`で宣言された`header`ブロックが呼び出される可能性があると予想される場合があります。 しかし、実際はそうではありません。 代わりに、`parent.mako`は`partials.mako`を呼び出し、`partials.mako`は`partials.mako`の `header`を呼び出し、レンダリングを終了します。 `child.mako`からは何もレンダリングされません。 `child.mako`の`header`ブロックと`partials.mako`の`header`ブロックの間に相互作用はありません。

代わりに、 `parent.mako` は継承構造を明示的に指定する必要があります。 `partials.mako`の特定の要素を呼び出すために、名前空間として呼び出します。

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

この場合、 `parent.mako` は、`child.mako`が参加する継承構造を示しています。 `partials.mako`は、名前ごとに使用できる定義/ブロックのみを定義します。

別のシナリオを以下に示します。これにより、 `child.mako` ドキュメントに対して両方の `SectionA` ブロックがレンダリングされます。

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

イメージは似ています。 ` <%include>` を使用する代わりに、名前空間を使用して`child.mako`のブロックを呼び出します。

```
 ## parent.mako
 <%inherit file="base.mako">
 <%namespace name="child" file="child.mako">

 <%block name="SectionA">
     ${child.SectionA()}
 </%block>
```

### 継承可能な属性
 `Namespace` オブジェクトの`Namespace.attr`アクセサーを使用すると、テンプレートで宣言されたモジュールレベルの変数にアクセスできます。 `self.attr` にアクセスすることで、`<%!...%>` セクションで宣言されている継承チェーンから通常の属性にアクセスできます。
 html
```
 <%!
     class_ = "grey"
 %>

 <div class="${self.attr.class_}">
     ${self.body()}
 </div>
```

継承するテンプレートが `class_` をオーバーライドして `white` になる場合の例。

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

