Cheetah:テンプレートファイルのデバッグ
=================
## パーサー/コンパイラーへの指示
### #breakpoint

```
書式
  #breakpoint
```

  `#breakpoint` ディレクティブは、特定のポイントで解析を停止するようにパーサーに指示するデバッグツールです。 それ以降のすべてのソースコードは無視されます。

  `#breakpoint` と `#stop` の違いは、 `#stop` は通常のテンプレート、例えば `#if` ブロック内などで発生しますが、 `#breakpoint` はCheetahのデバッグ時にのみ使用されることです。 もう1つの違いは、 `#breakpoint` はコンパイル時に動作し、 `#stop` は実行時にテンプレートの入力中に実行されることです。

### #compiler-settings

```
書式
  #compiler-settings
  key = value    (no quotes)
  #end compiler-settings

  #compiler-settings reset
```

  `#compiler-settings` ディレクティブは、Cheetahの標準設定を上書きし、ソースコードの解析方法とPythonコードの生成方法を変更します。 これにより、特定のテンプレートまたはテンプレートの一部内でCheetahのパーサー/コンパイラの動作を変更できます。

  `reset` 引数は設定をデフォルトに戻します。  `reset` は、終了タグはありません。

いくつかの例です：

```
 $myVar
 #compiler-settings
 cheetahVarStartToken = @
 #end compiler-settings
 @myVar
 #compiler-settings reset
 $myVar
```


```
 ## normal comment
 #compiler-settings
 commentStartToken = //
 #end compiler-settings

 // new style of comment

 #compiler-settings reset

 ## back to normal comments
```


```
 #slurp
 #compiler-settings
 directiveStartToken = %
 #end compiler-settings

 %slurp
 %compiler-settings reset

 #slurp
```

変更できる設定の一部を次に示します。

- 構文設定
 - cheetahVarStartToken
 - commentStartToken
 - multilineCommentStartToken
 - multilineCommentEndToken
 - directiveStartToken
 - directiveEndToken
- コード生成設定
 - ommentOffset
 - outputRowColComments
 - defDocStrMsg
 - useNameMapper
 - useAutocalling
 - reprShortStrConstants
 - reprNewlineThreshold

## トラブルシューティング
この章には、他のどこにも収まらない短いものが含まれています。

より専門的な問題とトラブルシューティングのヒントについては、CheetahFAQを参照してください。 ユーザーから提供された最近のヒントについては、定期的にwikiを確認してください。 行き詰まり、これらのリソースのどれも役に立たない場合は、メーリングリストで質問してください。

### プレースホルダーのヒント
明らかではない可能性のある特定の重要なルックアップを実行する方法は次のとおりです。 それぞれについて、最初にCheetah式を示し、次にPythonに相当するものを示します。これは、これらをテンプレートまたは純粋なPythonサブクラスのいずれかで使用できるためです。 Cheetahの例では、NameMapperショートカット（均一なドット表記、自動呼び出し）を可能な限り使用しています。

searchListに変数が存在するかどうかを確認するには次のようにします。

```
 $varExists('theVariable')
 self.varExists('theVariable')
```

これは、変数が存在しない場合に  `#NameMapper.NotFound` エラーを回避するため、 `#if` または `#unless` 構文で便利です。たとえば、ブラウザからの操作では通常は提供されるはずのCGI GETパラメータが、ユーザーがURLを手動で入力してパラメータを与えなかったような場合です。
  `hasVar()` メソッドは、 `varExists()` メソッドと同じです。

Pythonメソッドから  `searchList` で変数を検索するには：
 html
```
 self.getVar('theVariable')
 self.getVar('theVariable', myDefault)
```

これは、テンプレートの  `$theVariable` と同等です。 変数が欠落している場合、2番目の引数 `myDefault` が存在する場合はそれを返し、2番目の引数がない場合は `NameMapper.NotFound` を発生させます。 ただし、通常は、必要なすべての `searchList` 値がメソッド引数として入力されるようにメソッドを作成する方が簡単です。 そうすれば、呼び出し元は `$placeholder` を使用して引数を指定できます。これは、 `getVar()` 呼び出しを作成するよりも冗長ではありません。

変数が欠落している場合にデフォルト値を返す「安全な」プレースホルダールックアップを実行するには、次のようにします。

```
 $getVar('theVariable', None)
 $getVar('theVariable', $myDefault)
```

環境変数を取得するには、os.environモジュールをコンテナとして  `searchList` に配置します。または、Pythonコードで `envvar` を読み取り、その変数を設定します。

  `searchList` の前半にある変数は、後の `searchList` オブジェクトにある同じ名前の変数をオーバーライドすることに注意してください。os.environ、CGIパラメータなどで必要な変数以外の変数を含むオブジェクトを追加するときは注意してください。 その他の変数は、アプリケーションが依存する変数をオーバーライドして、バグを見つけるのが困難になる場合があります。また、ユーザーが不注意または悪意を持って予期しない環境変数またはCGIパラメータを設定し、プログラムを台無しにする可能性があります。これをすべて回避するには、名前空間に何が含まれているかを把握し、最も制御しやすい名前空間を最初に配置します。ユーザー指定のその他の変数を含む可能性のある名前空間の場合、名前空間自体を `searchList` に含めないでください。代わりに、必要な変数を独自の「安全な」名前空間にコピーします。

## 診断出力
デバッグ出力を自分に送信する必要がある場合は、{＃silent}を使用して標準エラーに出力できます。

```
 #silent $sys.stderr.write("Incorrigible var is '$incorrigible'.\n")
 #silent $sys.stderr.write("Is 'unknown' in the searchList? " +
     $getVar("unknown", "No.") + "\n" )
```

### Pythonメソッドを使用する場合
メソッドをCheetah の  `#def` メソッドとしてコーディングするかPythonメソッド（テンプレートが継承するクラスにあるPythonメソッド）としてコーディングするかを、選択することができます。
では、どのように選択すればよいのでしょうか？

一般に、メソッドが主にテキストとプレースホルダーで構成されている場合は、Cheetahメソッド  `#def` メソッド）を使用します。そのため、 `#def` が存在し、これらの種類のメソッドを作成する手間を省きます。また、いくつかの変数を `#set` するための `#if` スタンザがいくつかあり、その後に `#for` ループが続く場合、大したことはありません。ただし、メソッドの大部分がディレクティブで構成され、テキストが少ない場合は、Pythonで作成することをお勧めします。特に、チーターの方法で `#set` 、 `#echo` 、 `#silent` が広範囲に使用されていることに注意してください。これは、おそらく間違った言語を使用していることを示しています。もちろん、必要に応じて自由に行うことができます。

Cheetahで実行することがが難しいもう1つのことは、隣接またはネストされた複数行の構文、つまり  `#end` ディレクティブを伴うすべてのディレクティブです。 Pythonはインデントを使用してネストされたスタンザの開始と終了を表示しますが、Cheetahはインデントが出力に表示されるため、これを行うことはできません。したがって、出力内のこれらの余分なスペースとタブがすべて受け入れられる場合を除いて、ディレクティブを左マージンまたは前のテキストと同じ高さに保つ必要があります。
これに対応するために、  `#indent` ディレクティブが開発中でがまだリリースされていません。

最も難しいことはは、相反する目標がある場合に起こります。メソッドがその出力を部分的に生成、つまり、出力の連結をして、多くの  `searchList` 変数と多くのテキストを含み、複数行の構文
（  `#if ... #set ...#else #set ... #endif` など）を必要とする場合です。
Cheetahメソッドはいくつかの点でより有利ですが、ほとんどの場合はPythonメソッドが有利です。選択する必要があるのは、おそらくメソッドのグループをすべて同じ方法でコーディングすることです。または、メソッドを2つ（1つはチーターと1つはPython）に分割し、一方のメソッドでもう一方のメソッドを呼び出すこともできます。通常、これは、必要な値を計算するためにPythonメソッドを呼び出すCheetahメソッドを意味し、Cheetahメソッドが出力を生成します。ただし、発生する可能性のある問題の1つは、  `#set` は現在ステートメントごとに1つの変数しか設定できないため、PythonメソッドがCheetahメソッドに複数の値を返す必要がある場合は、別の方法で行う必要があります。

### スーパークラスメソッドの呼び出し
テンプレートまたは純粋なPythonクラスが  `Template` クラスまたはそのベースクラスの1つの標準メソッドまたはアトリビュートをオーバーライドする場合、多くのものが壊されれないように、メソッドでスーパークラスメソッドを呼び出す必要があります。オーバーライドする最も一般的なメソッドは、 `awake()` と `.__init__()` メソッドです。  `awake()` は、Webトランザクションの早い段階でWebwareによって自動的に呼び出されるため、テンプレートに必要なPython初期化コードを配置するのに便利な場所になります。スーパークラスの `awake()` は、CGI入力フィールドにアクセスするためのアトリビュートやメソッドなどを設定するため、間違いなく呼び出す必要があります。

スーパークラスメソッドの呼び出しにチーター固有のものはありませんが、それは不可欠であるため、ここでは標準のPythonテクニックを要約します。 Cheetahクラスは古いスタイルであるため、古いスタイルのクラスのソリューションについてのみ説明します。

```
 from Cheetah.Template import Template
 class MyClass(Template):
     def awake(self, trans):
         Template.awake(self, trans)
         ... great and exciting features written by me ...
```

スーパークラス名のハードコーディングを回避するために、この関数  `callbase()` を使用できます。この関数は、Pythonの `super()` をエミュレートします。  `super()` が存在する場合でも機能するため、アップグレード時にサーブレットをすぐに変更する必要はありません。 引数の順序は `super` が使用するものとは異なることに注意してください。

```
 ===========================================================================
 # Place this in a module SOMEWHERE.py .  Contributed by Edmund Lian.
 class CallbaseError(AttributeError):
     pass

 def callbase(obj, base, methodname='__init__', args=(), kw={},
     raiseIfMissing=None):
     try: method = getattr(base, methodname)
     except AttributeError:
         if raiseIfMissing:
             raise CallbaseError, methodname
         return None
     if args is None: args = ()
     return method(obj, *args, **kw)
 ===========================================================================
 # Place this in your class that's overriding .awake (or any method).
 from SOMEWHERE import callbase
 class MyMixin:
         def awake(self, trans):
                 args = (trans,)
                 callbase(self, MyMixin, 'awake', args)
                 ... everything else you want to do ...
 ===========================================================================
```


## テンプレートの最適化
テンプレートの入力を速くし、ユーザーのCPUサイクルを少なくするためにできることがいくつかあります。ただし、これに多くのエネルギーを投入する前に、本当に必要であることを確認してください。多くの場合、テンプレートは瞬時に初期化および入力されるように見えるため、最適化は必要ありません。テンプレートの入力が遅い、メモリの消費量が多すぎる、またはCPUサイクルが多すぎるという状況を見つけた場合は、メーリングリストでお知らせください。

値が頻繁に変更されない  `$変数` をキャッシュします。

非常に頻繁に使用される値には  `#set` ディレクティブを使用します。特に、深くネストされた構造やデータベースルックアップなどのコストのかかる操作から生じる場合はそうです。 `#set` 変数はPythonローカル変数に設定されます。Pythonローカル変数は、PythonグローバルまたはCheetahの `searchList` の値よりもルックアップ時間が速くなります。

変数ルックアップをPythonコードに移動すると、特定の状況でスピードアップが得られる場合があります。   `self` 属性を読んでいるだけの場合は、NameMapper の `lookup($変数)` を使用する理由はありません。 NameMapperは、単に `self` 属性を検索するよりもはるかに多くの作業を行います。

一方、値がどこから来るのか正確にわからない場合（  `self` から、 `searchList` から、CGI入力変数からなど）、その引数を自分の引数にする方が簡単です。メソッドを実行すると、テンプレートはすべてのNameMapperルックアップを処理できます。

```
 #silent $myMethod($arg1, $arg2, $arg3)
```


## テンプレートを別のテンプレートから呼び出す
Cheetahテンプレートは、実際には偽装したPythonモジュールです。 つまり、Cheetahがテンプレートをロードすると、それをPythonコードにコンパイルしてからバイトコードにコンパイルします。 すべてのテンプレートは単一のクラスとしてコンパイルされます。 重要なのは、ソースコードもバイトコードもファイルに自動的に保存されないということです。

ユーザーが1つのテンプレート（つまりPythonモジュール）を別のテンプレートからインポートできるようにする方法はいくつかあります。

1.ユーザーは、cheetahコンパイルコマンドラインプログラムを使用して、テンプレートを  `* .py` ファイルにコンパイルできます。 次に、インポートはPythonレベルで機能します。

編集後にすべてのテンプレートを半自動でコンパイルするには、次のGNU Makefileを使用できます。

 Makefile
```
.SUFFIXES: # Clear the suffix list
.SUFFIXES: .py .tmpl

%.py: %.tmpl
    cheetah compile --nobackup $<
    python -m compile $@

templates = $(shell echo \*.tmpl)
modules = $(patsubst %.tmpl,%.py,$(templates))

.PHONY: all
all: $(modules)
```

注意：Makefileでは、スペースではなくタブでインデントする必要があります。

2. Pythonインポートを無効にして、インポートフックを使用してCheetahを* .tmplファイルから直接インポートします。

コード例：

```
 from Cheetah import ImportHooks
 ImportHooks.install()

 import sys
 sys.path.insert(0, 'path/to/template_dir')  # or sys.path.append
```

importHooksは、*。pyc、*。py、および* .tmplからインポートしようとします-最初に見つかったものは何でも。 ImportHooksは、*。tmplを* .pyおよび* .pycに自動的にコンパイルします。

### Makefile
プロジェクトに複数のテンプレートがあり、「cheetah compile FILENAME.tmpl」と常に入力することにうんざりしていて、いつ入力するコマンドを覚えていない場合は、システムで{make}コマンドを使用できるようにすることを検討してください。 生活が楽になります。

これは、ErrorsTemplateとInquiryTemplateの2つのテンプレートを制御する単純なMakefileです。 {inquiry}と{receive}の2つの外部コマンドは、ErrorsTemplate.pyに依存しています。 さらに、InquiryTemplate自体はErrorsTemplateに依存しています。

 Makefile
```
all:  inquiry  receive

.PHONY:  all  receive  inquiry  printsource

printsource:
    a2ps InquiryTemplate.tmpl ErrorsTemplate.tmpl

ErrorsTemplate.py:  ErrorsTemplate.tmpl
    cheetah compile ErrorsTemplate.tmpl

InquiryTemplate.py:  InquiryTemplate.tmpl ErrorsTemplate.py
    cheetah compile InquiryTemplate.tmpl

inquiry: InquiryTemplate.py  ErrorsTemplate.py

receive: ErrorsTemplate.py
```

これで、いつでも  `make` を実行すると、変更されていないテンプレートは無視して、変更されたすべてのテンプレートが再コンパイルされます。または、 `make receive` と入力して、 `receive` に必要なすべてのテンプレートを再コンパイルできます。または、 `make ErrorsTemplate` と入力して `ErrorsTemplate` のみを再コンパイルできます。別のターゲット `printsource` は、プロジェクトのソースファイルを `Postscript` フォーマットに変換してプリンタに送信します。  `.PHONY` ターゲットは、そのターゲットのファイルは生成しないという事を make に指示するものです。

## マルチスレッドアプリケーションでのCheetahの使用
  `Template` クラスは、スレッド間で自由に共有できます。ただし、次のいずれかを行わない限り、 `Template` インスタンスを共有しないでください。

- 排他制御のためにロックを使用してテンプレートのレンダリングをシリアル化し、2つのスレッドが同時にテンプレートをレンダリングするのを防ぐようにします。
- スレッドセーフな機能を回避します。
-   `searchList` 値またはインスタンス変数の変更。
- キャッシングの使用（  `$* var` 、 `#cache` ディレクティブなど）。
-   `#set global` 、 `#filter` 、 `#errorCatcher`

1つのスレッドでこれらに変更が加えられると、他のスレッドでも表示されるため、出力に一貫性がなくなります。

テンプレートインスタンスを共有することの唯一の利点は、プレースホルダーキャッシュを構築することです。ただし、テンプレートインスタンスはオーバーヘッドが非常に低いため、各スレッドが独自のテンプレートインスタンスをインスタンス化するのにそれほど長くはかからないでしょう。テンプレートに1秒間に数回入力する場合にのみ、時差が大きくなるか、一部のプレースホルダーが非常に遅い計算をトリガーする場合（たとえば、毎回長いテキストファイルを解析する場合）。 Cheetahの最大のオーバーヘッドは、最初に  `Template` モジュールをインポートすることですが、これは、長時間実行されるアプリケーションで1回だけ実行する必要があります。

ロックにはPythonのmutexモジュール、または同様の相互排除のモジュールが使用できます。各レンダリングの前に  `searchList` 値またはインスタンス変数をレンダリングする必要がある場合（通常はそうです）、これを行う前にロックを設定し、レンダリングが完了した後にだけロックを解除します。

### gettextでCheetahを使用する
[gettext](https://www.gnu.org/software/gettext/])は、国際化されたアプリケーションを作成するためのプロジェクトで、Python でも標準モジュール [gettext](https://docs.python.org/ja/3/library/gettext.html])として提供されています。
gettextをCheetahとともに使用すると、CJK文字セットの場合でも、国際化されたアプリケーションを作成できますが、次の点に注意する必要があります。

- xgettextは、テンプレート自体ではなく、コンパイルされたテンプレートで使用されます。

NameMapper構文がPythonにコンパイルされる方法は、xgettextが認識する構文の邪魔になります。したがって、関数  `_()` 、 `N_()` 、およびngettextには特別な場合があります。翻訳用の文字列をマークするために別の関数セットを使用する必要がある場合は、Cheetah設定  `gettextTokens` を、翻訳用の文字列をマークするために使用している関数の名前を表す文字列のリストに設定する必要があります。


