Cheetah:ディレクティブ
=================

### ディレクティブ構文規則
ディレクティブタグはハッシュ文字（ `＃` ）で始まり、コメント、ループ、条件付きブロック、インクルード、およびその他すべての高度な機能に使用されます。 Cheetahは、ディレクティブタグ内でPythonに似た構文を使用し、有効なPython式を理解します。 {ただし、Pythonとは異なり、Cheetahはコロン（ `:` )とインデントを使用して複数行のディレクティブをマークしません。}これは、テキストの一部として空白が重要な環境では機能しません。代わりに、`{# for}` のような複数行のディレクティブには、対応する終了タグ（ `{#end for}` ）があります。ほとんどのディレクティブは、Pythonステートメントの直接のミラーです。

多くのディレクティブには、開始タグの後に引数があります。これは、タグに指定された構文である必要があります。すべての終了タグの構文は次のとおりです。

```
 #end TAG_NAME [EXPR]
```

式は無視されるため、基本的にはコメントです。

### ディレクティブクロージャと空白の処理
ディレクティブタグは、シャープ記号（ `＃` ）で明示的に閉じるか、省略した場合は暗黙的に行末で閉じることができます。

```
 #block testBlock #
 ブロックディレクティブの
 本文のテキスト
 #end block testBlock #
```

これは、次と同じです。

```
 #block testBlock
 ブロックディレクティブの
 本文のテキスト
 #end block testBlock
```

ディレクティブタグを明示的に閉じると、同じ行に他のテキストを続けることができます。

```
 bah, bah, #if $sheep.color == 'black'# black#end if # sheep.
```

ディレクティブタグが行の終わりで暗黙的に閉じられると、改行文字を含め、末尾の空白がすべて捨てられます。

```
 """
 foo #set $x = 2
 bar
 """
 outputs
 """
 foo bar
 """

 while
 """
 foo #set $x = 2 #
 bar
 """
 outputs
 """
 foo
 bar
 """
```

ディレクティブタグが暗黙的に閉じられ、その行に他のテキストがない場合、前の空白を含めて行全体が取り込まれます。

```
 """
 foo
    #set $x = 2
 bar
 """
 outputs
 """
 foo
 bar
 """

 while
 """
 foo
  - #set $x = 2
 bar
 """
 outputs
 """
 foo
  - bar
 """
```



## 出力の生成
### #echo
 `#echo` は複雑な式からの出力します。
>書式
> #echo EXPR

 `#echo` ディレクティブは、単純な`$変数`として記述できない式からの出力をエコーするために使用されます。

```
 Here is my #echo ', '.join(['silly']*5) # example
```

これは、次のようにレンダリングされます。

```
 Here is my silly, silly, silly, silly, silly example.
```

### #silent
 `#silent` は出力なしで式を実行します。
>書式
> #silent EXPR

 `#silent` は`#echo`とは異なり式は実行しますが、その出力は破棄します。

```
 #silent $myList.reverse()
 #silent $myList.sort()
 Here is #silent $covertOperation() # nothing
```

テンプレートで最初にPythonコードを実行する必要がある場合、たとえば、変数の値の計算、データベースへのアクセスなど、継承する `doEverything()` メソッドに配置し、テンプレートの上部で`#silent`を使用してこのメソッドを呼び出すことができます。


### #raw
>書式
> #raw
> #end raw

 `#raw ...#end raw` タグペア内にあるテンプレート定義のセクションは、`$変数` やその他のディレクティブを解析せずに逐語的に出力されます。 これは、デバッグやCheetahの例やチュートリアルに非常に役立ちます。

 `#raw` は、概念的にはHTMLの`<PRE>`タグとLaTeXの`verbatim {}`タグに似ていますが、これらのタグとは異なり、`#raw`によって本文が特別なフォントや書体で表示されることはありません。 Cheetahはフォントについて何も意識しないし、それが何であるかを知らないためです。


### #slurp
>書式
> #slurp

 `#slurp` ディレクティブは、表示されている行の末尾の改行を捨てて、次の行を現在の行に結合します。

ディレクティブの外側のスペースは、記述どおりに、そのまま出力されます。 前述のblack sheepの例では、 `black` の前と `sheep` の前にスペースがあります。 したがって、1行に複数のディレクティブを配置することはできますが、読みにくくなる場合があります。

```
 #if $a# #echo $a + 1# #end if
       - 各ディレクティブの間にスペースがあるか、
         合計2つの余分なスペースがあります。
 #if $a##echo $a + 1##end if
       - スペースはありませんが、##がコメントマーカーではないことを
         確認するために注意深く調べる必要があります。
 #if $a##echo $a + 1##end if     ### A comment.
       - ### では、最初の ＃ がディレクティブを終了し、続く2つの ## がコメントを開始します。
        これは、出力に影響を与えずにディレクティブタグに空白を追加する方法も示しています。
 #if $a##echo $a + 1##end if     # ## A comment.
       - 読みやすくなりましたが、コメントの前にスペースがあります。
```


これは、 `#for` ループで特に役立ちます。

```
 #for $i in range(5)
 $i #slurp
 #end for
```

これは次のようにレンダリングされます。

```
 0 1 2 3 4
```

## 変数への値のセット
### #set
>書式
> #set [global] $var = EXPR

 `#set` は、実行時にローカル変数を作成および更新するために使用されます。 式は任意のPython式にすることができます。 リスト内包表記の中間結果の一部でない限り、変数名の前に `$` を付けることを忘れないでください。

ここではいくつかの例を示します。

```
 #set $size = $length * 1096
 #set $buffer = $size + 1096
 #set $area = $length * $width
 #set $namesList = ['Moe','Larry','Curly']
 #set $prettyCountry = $country.replace(' ', '&nbsp;')
```

 `#set 変数` は、`$deeply.nested.value`、計算、または値の印刷可能なバージョンに短い名前を割り当てるのに役立ちます。 上記の最後の例では、`country`値のスペースをHTMLのノーブレークスペースエンティティに変換して、値全体がブラウザの1行に表示されるようにします。

 `#set 変数` は `#if` ディレクティブでも役立ちますが、複雑な論理ルーチンはCheetahではなくPythonでコーディングする必要があることに注意してください。


```
 #if $size > 1500
   #set $adj = 'large'
 #else
   #set $adj = 'small'
 #end if
```

または、Pythonの1行に相当する記述  `A and B or C` という記述もできます。 この場合、Bは真値でなければならないことに注意してください。
繰り返しますが、真値は、ゼロ( `0` )、`None`、空の文字列(`''`)、空のリスト(`[]`)、空の辞書(`{}`)以外のものを言います。
```
 #set $adj = $size > 1500 and 'large' or 'small'
```

>[! 注意] ：Cheetahの1行表記の `#if` は、変数を設定するのではなく出力を生成するため、このようには機能しません。

拡張代入演算子を使用することもできます。

```
 ## Increment $a by 5.
 #set $a += 5
```

デフォルトでは、 `global` アトリビュートを使用しない限り、`#set 変数`はメソッド呼び出しまたはインクルードファイルに表示されません。例：`#set global $var = EXPRESSION`
グローバル変数は、すべてのメソッド、ネストされたテンプレート、およびインクルードされたファイルに表示されます。 この機能は、予期しない事態を防ぐために注意して使用してください。

### #del
>書式
> #del $var

 `#del` は`#set`の反対の挙動を示すものです。 設定されているローカル変数を削除します。 その使用法は、Pythonの`del`文と同じです。

```
 #del $myVar
 #del $myVar, $myArray[5]
```

削除できるのはローカル変数のみです。  `#set global 変数` 、`searchList`変数、またはその他のタイプの変数を削除することはできません。

### #attr
>書式
> #attr $var = EXPR

 `#attr}` ディレクティブは、生成されたPythonクラスにクラスアトリビュートを作成します。 数字や文字列などの単純なPythonリテラルを割り当てるために使用する必要があります。 特に、式は`searchList`の値または`#set 変数`に依存する必要があります。これらはコンパイル時に認識されないためです。

```
 #attr $title = "Rob Roy"
 #attr $author = "Sir Walter Scott"
 #attr $version = 123.4
```

このテンプレートまたは任意の子テンプレートは、次のように値を出力できます。

```
 $title, by $author, version $version
```


テンプレートがテンプレートモジュール（ `*.py` )にコンパイルされていると仮定すると、
[etexts](http://www.gutenberg.org/]) から派生したテンプレートのライブラリがある場合は、タイトルと作成者を抽出してデータベースに配置できます。

### #def
>書式
> #def METHOD[(ARGUMENTS)]
> #end def
>
> #def METHOD[(ARGUMENTS)] : TEXT_AND_PLACEHOLDERS

 `#def` ディレクティブは、生成されたPythonクラスで新しいメソッドを定義するため、またはスーパークラスメソッドをオーバーライドするために使用されます。 これは、Pythonの`def`文に類似しています。 ディレクティブ自体は出力を生成しません。 ただし、メソッドが後で`$変数`によって呼び出されるたびに、メソッドのコンテンツが出力（および実行されるディレクティブ）に挿入されます。

```
 #def myMeth()
 これはサンプルのメソッドのテキストです
 $a $b $c(123)  ## これらの変数名は他の場所で定義されています
 #end def

 ## メソッドの使用
 $myMeth()
```

引数と括弧は省略できます。

```
 #def myMeth
 これはサンプルのメソッドのテキストです
 $a $b $c(123)
 #end def

 ## メソッドの使用
 $myMeth
```

Pythonの場合と同様に、メソッドには引数を指定でき、それらの引数のデフォルトを設定できます。 変数名の前の `$` を忘れないようにしてください。

```
 #def myMeth($a, $b=1234)
 これはサンプルのメソッドのテキストです
 $a - $b
 #end def

 ## メソッドの使用
 $myMeth(1)
```

この最後の例からの出力は次のようになります。

```
 これはサンプルのメソッドのテキストです
 1 - 1234
```

 `#def` ディレクティブの1行バージョンもあります。 {複数行のディレクティブとは異なり、コロン（`:`)を使用してメソッドのシグネチャと本文を区切ります。

```
 #attr $adj = 'trivial'
 #def myMeth: これは $adj メソッドです
 $myMeth
```

先頭と末尾の空白はメソッドから削除されます。 これは、以下とは対照的です。

```
 #def myMeth2
 これは $adj メソッドです
 #end def
```

ここで、メソッドには `'メソッドです'` の後に改行が含まれます。 改行が必要ない場合は、`#slurp`を追加します。

```
 #def myMeth3
 これは $adj メソッドです#slurp
 #end def
```

 `#def` はコンパイル時に処理されるため、それを呼び出すプレースホルダーの上または下に表示される可能性があります。また、スーパークラスプレースホルダーがサブクラスでオーバーライドされたメソッドを呼び出す場合、呼び出されるのはサブクラスメソッドです。

### #block ... #end block
 `#block` ディレクティブを使用すると、サブクラスで選択的に再実装できるテンプレートのセクションにひとつの単位として扱うことができます。全体をコピーして貼り付けて編集しなくても、テンプレートの一部を変更するのに非常に便利です。ブロックを使用するテンプレート定義からの出力は、`#block ... #endblock` ディレクティブが削除された同じテンプレートからの出力と同じになります。

>[! 注意]：一般的な単語の  `block` と混同しないようにしてでください。
> これは、 `何かの文字列#TAG ... #end TAG` ペア内のコードのセクションを意味します。
> したがって、 `if` ブロック、`for`ブロック、`def`ブロック、`block`ブロックなど。
> ここでは、 `block` ブロックについてのみ説明します。

ブロックを再実装するには、 `#def` ディレクティブを使用します。この効果は、再実装の場所ではなく、元のブロックが定義された時点に戻って出力テキストを変更するように見えることです。

```
 #block testBlock
 コンテンツのテキスト
 ブロックディレクティブの領域
 #if $testIt
 $getFoo()
 #end if
 #end block testBlock
```

必要に応じて、 `#endblock` ディレクティブでブロック名を繰り返すかどうかを指定できます。

 `#block` ディレクティブは任意の深さにネストできます。

```
 #block outerBlock
 外側のブロック（outerBlock)の内容

 #block innerBlock1
 内側のブロック(innerBlock1)の内容
 #end block innerBlock1

 #block innerBlock2
 内側のブロック(innerBlock2)の内容
 #end block innerBlock2

 #end block outerBlock
```

 `#endblock` ディレクティブのブロック名はオプションであることに注意してください。

技術的には、 `#block` ディレクティブは、`#def`ディレクティブの直後の同じ名前のブロック名が続くことと同等です。 実際、これはCheetahが内部で処理していることです。 つまり、テンプレートの他の場所で `$ブロック名` を使用して、ブロックコンテンツを再度出力できます。

1行の `#def` に類似した1行の`#block`構文があります。
ブロックは引数を必要とするべきではありません

## 外部ファイルの取り込み
### #include
>書式
> #include [raw] FILENAME_EXPR
> #include [raw] source=STRING_EXPR

 `#include` ディレクティブは、テンプレート定義の外部からのテキストを含めるために使用されます。 テキストは、外部ファイルまたは`$変数`から取得できます。 Cheetahは、外部ファイルを操作するときに、含まれているファイルへの変更を監視し、必要に応じて更新します。

この例は、外部ファイルでの使用法を示しています。

```
 #include "includeFileName.txt"
```

読み込まれる  `FileName.txt` の内容は、Cheetah によって解析されます。

次の例は、 `$変数` で読み込むファイル名を与える方法を示しています。

```
 #include source=$myParseText
```
 `$myParseText` の値は、Cheetahによって解析されます。 これは、テンプレート定義に変数タグ
 `$ myParseText` を単に配置することと同じではありません。 後者の場合、`$myParseText`の値は解析されません。

デフォルトでは、含まれているテキストはCheetahタグ用に解析されます。  `raw=` 引数を使用して、解析を抑制することができます。

```
 #include raw "includeFileName.txt"
 #include raw source=$myParseText
```
Cheetahは、ネストされた `Template` オブジェクト内に`#include`テキストの各チャンクをラップします。 ネストされた各テンプレートには、メインテンプレートのsearchListのコピーがあります。 ただし、`set`変数は、`#set global`キーワードを使用して定義されている場合にのみインクルード全体に表示されます。

すべてのディレクティブは、インクルードファイルでバランスを取る必要があります。 つまり、インクルード内で `#for` または`#if`ブロックを開始する場合は、同じインクルードで終了する必要があります。


### #import と #from
>書式
> #import MODULE_OR_OBJECT [as NAME] [, ...]
> #from MODULE import MODULE_OR_OBJECT [as NAME] [, ...]

 `#impor` }および`#from`ディレクティブは、外部Pythonモジュールまたはオブジェクトをプレースホルダーで使用できるようにするために使用されます。 構文はPythonのインポート構文と同じです。 インポートされたモジュールは、生成されたPythonクラスのすべてのメソッドにグローバルに表示されます。

```
 #import math
 #import math as mathModule
 #from math import sin, cos
 #from math import sin as _sin
 #import random, re
 #from mx import DateTime         # ## Part of Egenix's mx package.
```

上記のインポートの後、 `$math` 、`$mathModule`、`$sin`、`$cos`、`$_sin`、`$random`、`$ re`、`$DateTime`を`$変数`と式が利用することができます。

すべてのテンプレートは `Cheetah.Template.Template` のサブクラスです。 ただし、テンプレートが別のテンプレートまたは純粋なPythonクラスをサブクラス化することは可能です。 これは、`#extends` がステップインする場所です。親クラスを指定します。
Cheetahは、まだインポートしていない場合、 `#extends` ディレクティブに記載されているクラスを自動的にインポートします。 暗黙的なインポートは次のように機能します。


```
 #extends Superclass
 ## 暗黙的に '#from Superclass import Superclass'　と同じ

 #extends Cheetah.Templates.SkeletonPage
 ## 暗黙的に '#from Cheetah.Templates.SkeletonPage import SkeletonPage'　と同じ
```


### #extends
>書式
> #extends

スーパークラスが通常とは異なる場所にある場合、またはクラスとは異なる名前のモジュールにある場合は、明示的にインポートする必要があります。インポートされていないクラスからの拡張はサポートされていません。たとえば、文字列から動的に作成されたテンプレートから。親テンプレートをモジュールに取り込む最も実用的な方法はそれをプリコンパイルすることであるため、すべての親テンプレートは基本的にプリコンパイルする必要があります。

テンプレートには `#extends` ディレクティブを1つだけ含めることができ、クラスを1つだけリストすることができます。つまり、テンプレートは多重継承を行いません。これは意図的なものです。テンプレート内から複数の基本クラスを正しく初期化するのは非常に困難です。ただし、純粋なPythonクラスで多重継承を行うことができます。

純粋なPythonクラスが `__ init__()` や`awake()`などの標準の`Template`メソッドのいずれかをオーバーライドする場合は、必ずメソッドでスーパークラスメソッドを呼び出すようにしてください。そうしないと問題が発生します。スーパークラスメソッドの呼び出し例は、セクション`tips.callingSuperclassMethods`にあります。

いずれの場合も、ルートスーパークラスは `Template` である必要があります。最下位のクラスがテンプレートの場合は、その中の`#extends`を省略するだけで、`Template`から自動的に継承されます。 最下部のクラスが純粋なPythonクラスである場合、`Template`から明示的に継承する必要があります

```
 from Cheetah.Template import Template
 class MyPurePythonClass(Template):
     # ..
```

Pythonクラスを `Template` から継承することに関心がない場合は、クラスと`Template`の両方から継承する小さなグルークラスを作成します。

例を示す前に、Cheetahが継承ツリーをどのように構成するかを、**指示しない**ことを強調します。 上記のルールに従う限り、多くの構造が可能です。

これは、一般的なサイトテンプレートだけでなく、サイトのこのセクションのテンプレートと、各URLの特定のテンプレートサーブレットを含む大規模なWebサイトの例です。 各テンプレートは、テンプレートで使用されるメソッド/属性を含む純粋なPythonクラスから継承します。 最下位のスーパークラスから始めて、特定のテンプレートサーブレットで終わります。

```
 1.  SiteLogic.py (サイトのためのメソッドを含むPythonで実装されたクラス)
         from Cheetah.Template import Template
         class SiteLogic(Template):

 2.  Site.tmpl/py  (一般的なサイトフレームワークを含むテンプレート。
                    これは出力を制御するテンプレートです。
                    <HTML> <HEAD> ...を含むもの、
                    ＃def /＃blockの外側にテキストを含むもの)
         #from SiteLogic import SiteLogic
         #extends SiteLogic
         #implements respond

 3.  SectionLogic.py  (セクションのヘルパーコード含むPythonで実装されたクラス)
         from Site import Site
         class SectionLogic(Site)

 4.  Section.tmpl/py  (セクションの#defオーバーライドなどを含むテンプレート)
         #from SectionLogic import SectionLogic
         #extends SectionLogic

 5.  page1Logic.py  (テンプレートサーブレットのヘルパーコードを含むPythonで実装されたクラス)
         from Section import Section
         class indexLogic(Section):

 6.  page1.tmpl/py  (テンプレート-サイトの特定のページのサーブレット)
         #from page1Logic import page1Logic
         #extends page1Logic
```

純粋なPythonクラスには、直接の子テンプレートでは使用されないが、必要に応じて子孫テンプレートで使用できるメソッド/アトリビュートが含まれている場合もあります。 たとえば、サイトテンプレートには、サイト管理者の名前と電子メールアドレスの属性があり、必要なテンプレートで `$変数` としてすぐに使用できます。

 `#extends` を使用する場合は常に、上記の手順2のように`#implements`も必要になることがよくあります。 次のセクションを読んで、`#implements` とは何か、いつ使用するかを理解してください。

### #iimplements
 `#def` または`#block`メソッドを直接呼び出して、その出力を取得できます。 トップレベルのコンテンツ（`#def` / `#block`の外側にあるすべてのテキスト/プレースホルダー/ディレクティブ）は連結され、デフォルトで`respond()`メソッドにラップされます。 したがって、`respond()`を呼び出すと、**テンプレート全体の出力**が得られます。 したがって、Webwareが `respond()` を呼び出すと、テンプレート全体が出力されます。また、テンプレートインスタンスで`print()`または`str(t)`を実行すると、Cheetahが `__str__()`メソッドが呼び出されるメソッドのエイリアスにするという事実を利用しています。

それはすべて問題ありませんが、アプリケーションが  `respond()` ではなく別のメソッド名を呼び出すことを好む場合はどうでしょうか。 たとえば、代わりに `send_output()` を呼び出したい場合はどうなりますか？ そこで `#mplements` がステップインします。これにより、メインメソッドの名前を選択できます。 これをテンプレート定義に入れるだけです：


```
 #implements send_output
```

あるテンプレートが別のテンプレートを拡張する場合、継承チェーン内のすべてのテンプレートには独自のメインメソッドがあります。テンプレートに入力するには、これらのメソッドの1つだけを呼び出し、他のメソッドは無視されます。呼び出すメソッドは、アプリケーションの構造に応じて、継承チェーン内の任意のテンプレート（ベーステンプレート、リーフテンプレート、またはそれらの間）に含めることができます。したがって、2つの問題があります。（1）正しいメソッド名を呼び出すことと、（2）不要な同じ名前のサブクラスメソッドが呼び出したいメソッドをオーバーライドできないようにすることです。

Cheetahは、呼び出すメソッドが `respond()` であると想定しています。これは、Webwareが呼び出すものだからです。`#block`で適切に機能するため、目的のメソッドが最下位レベルのベーステンプレートのメソッドであると想定します。したがって、`#extends` を使用すると、Cheetahはそのテンプレートのメインメソッドを `writeBody()`に変更して、邪魔にならないようにし、ベーステンプレートの`respond()` をオーバーライドしないようにします。

残念ながら、テンプレートが他の方法で使用されている場合、この仮定は破綻します。たとえば、最高レベルのリーフテンプレートでメソッドを使用し、ベーステンプレートを単なるメソッド/属性のライブラリとして扱いたい場合があります。その場合、リーフテンプレートは、メソッド名を `respond()` （またはアプリケーションが呼び出したいもの）に戻すために`#implementsrespond`が必要です。同様に、メインメソッドが継承チェーンの中間テンプレートの1つにある場合、そのテンプレートには`#mplementsresponse`が必要です。

仮定が崩れるもう1つの方法は、ベーステンプレートのメインメソッドであるが、そのテンプレートが純粋なPythonクラスを拡張する場合です。 Cheetahは `#extends` を確認し、メソッドの名前を`writeBody()` に忠実に、しかし誤って変更するため `#implementsrespond` を使用して元に戻す必要があります。それ以外の場合は、`Cheetah.Template`内のダミーの`respond()`が見つかり、何も出力されません。 したがって、`#extends` を使用していて出力が得られない場合、{最初の}ことを考える必要があります。



## 制御構造
制御構造とは、プログラムのフロー制御をするすべてのものを指します。
Cheetah では次のフロー制御をサポートしています。

### #for ... #end for
 `{#for}` ディレクティブはシーケンスを繰り返し処理します。 構文はPythonと同じですが、変数の前のシャープ記号(`$`)を忘れないようにしてください。

> 書式
> #for $var in EXPR
> #end for


次のテンプレートは `#for` の簡単な例です。

```
 <TABLE>
 #for $client in $service.clients
 <TR>
 <TD>$client.surname, $client.firstname</TD>
 <TD><A HREF="mailto:$client.email" >$client.email</A></TD>
 </TR>
 #end for
 </TABLE>
```

辞書のキーと値をループする方法は次のとおりです。

```
 <PRE>
 #for $key, $value in $dict.items()
 $key: $value
 #end for
 </PRE>
```

ハイフンで区切られた番号のリストを作成する方法は次のとおりです。 この `#endfor` タグは、各ハイフンの後に改行文字が導入されないように、最後の行を共有します。

```
 #for $i in range(15)
 $i - #end for
```

 `{#end for}` の場所がインデンテーションの妥当性を損なう場合は、代わりに次のようにすることができます。

```
 #for $i in $range(15)
 $i - #slurp
 #end for
```

前の2つの例では、最後の番号の後に余分なハイフンを配置します。  `#set` ディレクティブを使用して、この問題を回避する方法を次に示します。これについては、以下で詳しく説明します。

```
 #set $sep = ''
 #for $name in $names
 $sep$name
 #set $sep = ', '
 #end for
```

文字列の間にセパレータを配置するだけですが、forループは必要ありません。

```
 #echo ', '.join($names)
```

### #repeat ... #end repeat
特定の回数何かをします。 引数は任意の数式にすることができます。 ゼロまたは負の場合、ループはゼロ回実行されます。
>書式
> #repeat EXPR
> #end repeat

次のテンプレートは `#repeat` の簡単な例です。

```
 #repeat $times + 3
 She loves me, she loves me not.
 #repeat
 She loves me.
```

ループ内では、どの反復を行っているかを判断する方法はありません。 カウンター変数が必要な場合は、Pythonの `range()` 関数で代わりに`#for`を使用してください。 Pythonの範囲はデフォルトでベース0であるため、1からカウントを開始する方法は2つあります。1から5までカウントしたいとし、`$count`は5です。

```
 #for $i in $range($count)
 #set $step = $i + 1
 $step.  Counting from 1 to $count.
 #end for


 #for $i in $range(1, $count + 1)
 $i.  Counting from 1 to $count.
 #end for
```

以前の実装では、繰り返しカウンターとしてローカル変数{$ i}を使用していました。 ただし、これにより `#repeat` のインスタンスがネストされなくなりました。 現在の実装では `#repeat` のすべてのインスタンスに新しいローカル変数を使用するため、この問題は発生しません。

### #while ... #end while
 `#while` はPythonの`while`文と同じです。 その後に任意のブール式を続けることができます。
>書式
> #while EXPR
> #end while

次のテンプレートは `#while` の簡単な例です。

```
 #while $someCondition('arg1', $arg2)
 条件式は真値
 #end while
```

無限ループを作成しないように注意してください。  `#while 1` は、コンピュータのメモリが不足するまでループすることになります。

### #break と #continue
これらのディレクティブは、Pythonと同様に使用されます。  `#break` は`#for`ループを途中で終了しますが、`#continue`はすぐに`#for`ループの次の反復にジャンプします。

>書式
> #break
> #continue


この例では、出力リストに `10 - ` は含まれません。

```
 #for $i in range(15)
 #if $i == 10
   #continue
 #end if
 $i - #slurp
 #end for
```

この例では、 `'Joe'` に等しい名前が見つかるとループが終了します。

```
 #for $name in $names
 #if $name == 'Joe'
   #break
 #end if
 $name - #slurp
 #end for
```


### #if ... #else if ... #else ... #end if
>書式
> #if EXPR
> #else if EXPR
> #elif EXPR
> #else
> #end if

 `#if` ディレクティブは、テキストの一部を条件付きで表示するために使用されます。 `#if` と `#elseif` の後に条件式を続ける必要がありますが、 `# else` には不要です。有効なPython式はすべて許可されます。 Pythonと同様に、ゼロ( `0` )、 空の文字列( `''` )、 `None` 、空のリスト( `[]` )、または空の辞書( `{}` )に評価されない限り、式は真値( `True` )です。 Pythonとは異なり、 `# elif` は  `#elseif`  の同義語として受け入れられます。

ここではいくつかの例を示します。

```
 #if $size >= 1500
 大きい
 #else if $size < 1500 and $size > 0
 小さい
 #else
 それら以外
 #end if
```


```
 #if $testItem($item)
 The item $item.name is OK.
 #end if
```

これは、 `#if` ディレクティブと `#for` ディレクティブを組み合わせた例です。

```
 #if $people
 <table>
 <tr>
 <th>Name</th>
 <th>Address</th>
 <th>Phone</th>
 </tr>
 #for $p in $people
 <tr>
 <td>$p.name</td>
 <td>$p.address</td>
 <td>$p.phone</td>
 </tr>
 #end for
 </table>
 #else
 <p> Sorry, the search did not find any people. </p>
 #end if
```


### 1行での#if
>書式
> #if EXPR1 then EXPR2 else EXPR3#

フロー制御のための `#if` ディレクティブには、1行で記述する方法もあります。 `EXPR1` が `True` の場合、 `EXPR2` を評価し、結果を出力します。（ `#echo EXPR2#` と同様の結果）。  `EXPR1` が `True` でない場合は、 `EXPR3` を評価し、その結果を出力します。 このディレクティブでは不要な式は評価されません。

Python の `if` 文でいうところの `then` と `else` の両方を含める必要があります。 これがうまくいかない場合や、このスタイルが気に入らない場合は、複数行の `#if` ディレクティブを使用してください。

末尾の `#` は、通常のディレクティブの終端文字です。 いつものように、同じ行のディレクティブの後に何もない場合は省略することができます。

### #unless ... #end unless
>書式
> #unless EXPR
> #end unless

 `#unless` は `#if` の反対の挙動をするものです。条件式が偽値( `False` )として評価される場合、テキストが実行されます。 ときによりこれはとても便利です。
 `#unless EXPR` は `#if not(EXPR)` と同等です。

```
 #unless $alive
 This parrot is no more!  He has ceased to be!
 'E's expired and gone to meet 'is maker! ...
 THIS IS AN EX-PARROT!!
 #end unless
```
 `#if` とは異なり、`#unless` 構造内で `#elseif` または `#else` を使用することはできません。

### #pass
>書式
> #pass

 `#pass` ディレクティブはPythonの `pass` ステートメントと同じです。何もしません。 文が構文的に必要であるが、プログラムがアクションを必要としない場合に使用できます。

次の例は、$ Aのみが真の場合は何もしません

```
 #if $A and $B
    do something
 #elif $A
   #pass
 #elif $B
   do something
 #else
   do something
 #end if
```

### #stop
 `#stop` ディレクティブは、特定の時点でテンプレートの処理を停止するために使用されます。 出力には、その時点までに処理されたものだけが表示されます。

 `#stop` が `#include` 内で呼び出されると、インクルードされた残りのコードをスキップして、
 `＃include` ディレクティブの後から続行します。 含まれているコードの処理を停止します。 同様に、 `#stop` が `#def` または `#block` 内で呼び出されると、 `#def` または `#block` のみが停止します。

```
 猫が
 #if 1
   マットの上に座った
   #stop
   ネズミを見ている
 #end if
 姿勢を低くして
```

これは次のようにレンダリングされます。
html
```
 猫が
   マットの上に座った
```

次の例では。

```
 猫が
 #block action
   マットの上に座った
   #stop
   ネズミを見ている
 #end block
 姿勢を低くして
```

出力は次のようになります。

```
 猫が
   マットの上に座った
 姿勢を低くして
```

### #return
これはPythonと同じように使用されます。  `#return` は、デフォルトの戻り値 `None` または指定された値で現在のメソッドを終了します。  `#def` または `#block` 内でのみ使用できます。

>書式
> #return


 `#return` は、呼び出されたメソッドから出力されたすべてのテキストの合計を返す `#stop` ディレクティブとは異なることに注意してください。 次の例は、この点を示しています。

```
 1
 $test[1]
 3
 #def test
 1.5
 #if 1
 #return '123'
 #else
 99999
 #end if
 #end def
```

これは次のようにレンダリングされます。

```
 1
 2
 3
```

一方次の例では。

```
 1
 $test
 3
 #def test
 1.5
 #if 1
 #stop
 #else
 99999
 #end if
 #end def
```


```
 1
 1.5
 3
```


## エラーハンドリグ

Cheetahでランタイムエラー（例外）を処理する方法は2つあります。 1つ目は、Pythonの構造化された例外処理ステートメントを反映するCheetahディレクティブを使用することです。 2つ目は、チーターの `ErrorCatcher` フレームワークです。 これらについて以下に説明します。

### #try ... #except ... #end
### #try ... #finally
### #assert

Cheetahの例外処理ディレクティブは、Pythonの例外処理ステートメントを正確に反映しています。 次のチーターコードは、それらの使用法を示しています。

```
 #try
   $mightFail()
 #except
   It failed
 #end try

 #try
   #assert $x == $y
 #except AssertionError
   They're not the same!
 #end try

 #try
   #raise ValueError
 #except ValueError
   #pass
 #end try


 #try
   $mightFail()
 #except ValueError
   Hey, it raised a ValueError!
 #except NameMapper.NotFound
   Hey, it raised a NameMapper.NotFound!
 #else
   It didn't raise anything!
 #end try

 #try
   $mightFail()
 #finally
   $cleanup()
 #end try
```

Pythonと同様に、 `#except` と `#finally` は同じ `try` ブロックに表示できませんが、ネストされた`try`ブロックには表示できます。


### #errorCatcher と ErrorCatcherオブジェクト
>書式
> #errorCatcher CLASS
> #errorCatcher $PLACEHOLDER_TO_AN_ERROR_CATCHER_INSTANCE

 `ErrorCatcher` は、`$placeholder` タグ内で発生する例外をキャッチし、開発者にカスタマイズ可能な警告を提供するデバッグツールです。 通常、最初に欠落している名前空間値は `NameMapper.NotFound` の例外を発生させ、テンプレートの入力を停止します。 これには、開発者が後続の出力を見ずに例外を順番に解決する必要があります。 `ErrorCatcher` を有効にすると、開発者はすべての例外とその周辺のテンプレート出力を一度に確認できます。

 `Cheetah.ErrorCatchers` モジュールは、`ErrorCatchers`のベースクラスを定義します。


```
 class ErrorCatcher:
     _exceptionsToCatch = (NameMapper.NotFound,)

     def __init__(self, templateObj):
         pass

     def exceptions(self):
         return self._exceptionsToCatch

     def warn(self, exc_val, code, rawCode, lineCol):
         return rawCode
```

この `ErrorCatcher` は、`NameMapper.NotFound` 例外をキャッチし、問題のあるプレースホルダーをテンプレート出力に未加工の形式で表示したままにします。

```
 #errorCatcher Echo
 #set $iExist = 'Here I am!'
 これは正しいプレースホルダー: $iExist
 これは間違ったプレスホールダー: $iDontExist
```

このテンプレートが実行された場合、出力は次のようになります。

```
 これは正しいプレースホルダー: Here I am!
 これは間違ったプレスホールダー: $iDontExist
```

 `Cheetah.ErrorCatchers` は、ありな方法でなしでしたするするの特殊なサブクラスももします。 `Cheetah.ErrorCatchers.Echo` 、 `Cheetah.ErrorCatchers.BigEcho` がいかされます

```
 Here's a good placeholder: Here I am!
 Here's bad placeholder: ===============&lt;$iDontExist could not be found&gt;===============
```

 `ErrorCatcher` はパフォーマンスに大きな影響を与え、デフォルトでオフになっています。 `Template` クラスの `errorCatcher` キーワード引数を使用してオンにすることもできます。 この引数の値は、 `Cheetah.ErrorCatchers` のどのクラスを使用するかを指定する文字列、または `Cheetah.ErrorCatchers.ErrorCatcher` をサブクラス化するクラスのいずれかである必要があります。 `#errorCatcher` ディレクティブを使用して、テンプレートの途中で `errorCatcher` を変更することもできます。

 `Cheetah.ErrorCatchers.ListErrors` は、後で取得できるエラーのリストを維持しながら、`Echo`と同じ出力を生成します。 リストを取得するには、 `Template` クラスの `errorCatcher()` メソッドを使用して `errorCatcher` を取得してから、その `listErrors()` メソッドを呼び出します。

 `ErrorCatcher` は、ディレクティブ内で発生した例外をキャッチしません。

