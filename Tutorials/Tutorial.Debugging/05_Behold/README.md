Beholdモジュールを使ってみよう
=================

## beholdモジュールについて
[behold ](https://github.com/robdmc/behold) は、大規模な Python プロジェクトのデバッグを容易にするパッケージです。Behold はコードベース全体でコンテキストデバッグを行うことができます。これは、あるモジュール内の状態を利用して、完全に異なるモジュールの印刷やステップデバッグを制御できることを意味します。多くの大規模なマルチファイルアプリケーション（Djangoを見ています）のステートフルな性質を考慮すると、この機能はデバッグワークフローの貴重なコントロールとなります。

Beholdは純粋なPythonで書かれており、依存関係はありません。

## インストール

behold の異インストールは pip コマンドで行います。

 bash
```
 $ pip install behold
```

### 使用方法

behold を使用するためには、まず次のようにインポートしておきます。


```
 from behold imort Behold
 
```

 `Behold` の別名として、 `B` と `BB` が定義されているため、次のようにすることもできます。


```
 from behold import B
```



```
 In [2]: # %load 01_print_object.py
    ...: from behold import Behold
    ...:
    ...: letters  = ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']
    ...:
    ...: for index, letter in enumerate(letters):
    ...:     # Behold の記述は次のコードと同じ
    ...:     # print('index: {}, letter: {}'.format(index, letter))
    ...:     _ = Behold().show('index', 'letter')
    ...:
 index: 0, letter: a
 index: 1, letter: b
 index: 2, letter: c
 index: 3, letter: d
 index: 4, letter: A
 index: 5, letter: B
 index: 6, letter: C
 index: 7, letter: D
 
 In [3]:
    
```


```
 In [2]: # %load 02_conditional_print.py
    ...: from behold import Behold
    ...:
    ...: letters  = ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']
    ...:
    ...: for index, letter in enumerate(letters):
    ...:     # Behold の記述は次のコードと同じ
    ...:     # if letter.upper() == letter and index % 2 == 0:
    ...:     #     print('index: {}'.format(index))
    ...:     _ = (Behold()
    ...:          .when(letter.upper() == letter and index % 2 == 0)
    ...:          .show('index'))
    ...:
 index: 4
 index: 6
 
 In [3]:
 
```


```
 In [2]: # %load 03_tagged_print.py
    ...: from behold import Behold
    ...:
    ...: letters  = ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']
    ...:
    ...: for index, letter in enumerate(letters):
    ...: # Behold の記述は次のコードと同じ
    ...: # if letter.upper() == letter and index % 2 == 0:
    ...: #   print('index: {}, letter:, {}, even_uppercase'.format(index, letter)
    ...: )
    ...: # if letter.upper() != letter and index % 2 != 0:
    ...: #   print('index: {}, letter: {} odd_lowercase'.format(index, letter))
    ...:
    ...:     _ = (Behold(tag='even_uppercase')
    ...:          .when(letter.upper() == letter and index % 2 == 0)
    ...:          .show('index', 'letter'))
    ...:     _ = (Behold(tag='odd_lowercase')
    ...:          .when(letter.lower() == letter and index % 2 != 0)
    ...:          .show('index', 'letter'))
    ...:
    ...:
 index: 1, letter: b, odd_lowercase
 index: 3, letter: d, odd_lowercase
 index: 4, letter: A, even_uppercase
 index: 6, letter: C, even_uppercase
 
 In [3]:
 
```


例えば、多くのディレクトリに多数のファイルを配置した複雑なコードベースを持っているとします。バグを追いかける過程で、特定の関数の中で起こっていることを印刷したいと思うかもしれません。しかし、その関数が、まったく別のファイルで定義された他の関数から呼び出されたときにだけ、印刷を行いたい。このような状況は、コードが複数のアプリにまたがっているような Django の Web プロジェクトで頻繁に発生します。これは、Behold が本当に輝くユースケースです。以下に簡単な例を挙げます。

あるモジュールのどこかにある再利用可能な関数をデバッグしたいとします。

 myfunc.py
```
 from behold import Behold
 
 def my_function():
     x = 'hello'  # 何かしらの処理
 
     # コンテキストが 'testing' のときだけ x の値を出力
     Behold().when_context(what='testing').show('x')
 
     # コンテキストが 'debugging' のといだけ、デバッガを起動
     if Behold().when_context(what='debugging').is_true():
         import pdb; pdb.set_trace()
         
```

これで、プロジェクトのどこかにある全く別のモジュールから、自分の関数がどのようにデバッグされるかをコントロールできるようになります。


```
 In [2]: # %load 04_contextual_explain.py
    ...: from behold import in_context
    ...: from myfunc import my_function
    ...:
    ...: # コンテキスト 'testing' でデコレート
    ...: @in_context(what='testing')
    ...: def test_x():
    ...:     my_function()
    ...: test_x()
    ...:
    ...: # 'debugging' をセットしたコンテキストマネージャ
    ...: with in_context(what='debugging'):
    ...:     my_function()
    ...:
 x: hello
 --Return--
 > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/Behold/myfunc.py(11)my_function()->None
 -> import pdb; pdb.set_trace()
 (Pdb)
 
```


## オブジェクトの属性を印刷する
ここまでは、ローカル変数の名前を表す文字列を引数にして、.show()メソッドを呼び出してきました。では、コードの中でオブジェクトの属性を出力したい場合はどうすればよいのでしょうか？以下の例では、Itemクラスのインスタンスを使用しています。


```
 n [2]: # %load 05_print_object_attr.py
    ...: from behold import Behold, Item
    ...:
    ...: item = Item(a=1, b=2, c=3)
    ...:
    ...: _ = Behold(tag='with_args').show(item, 'a', 'b')
    ...: _ = Behold(tag='no_args').show(item)
    ...:
 a: 1, b: 2, with_args
 a: 1, b: 2, c: 3, no_args
 
 In [3]:
 
```


## グローバル変数と入れ子になった属性の印刷
 `.show()` メソッドに文字列の引数を与えると、デフォルトの動作として、ローカル変数を調べて文字列に一致する名前を探します。グローバル変数はこの方法ではアクセスできません。さらに、入れ子になった属性を持つクラスがある場合、それらも単純な文字列引数ではアクセスできません。この例では、 `.show()` を使ってこれらのタイプの変数にアクセスする方法を説明します。


```
 In [2]: # %load 06_globals.py
    ...: from behold import Behold, Item
    ...:
    ...: # define a global variable
    ...: g = 'global_content'
    ...:
    ...: def example_func():
    ...:     employee = Item(name='Toby')
    ...:     boss = Item(employee=employee, name='Michael')
    ...:
    ...:     print('# グローバル変数は参照できない')
    ...:     Behold().show('boss', 'employee', 'g')
    ...:
    ...:     print('\n#上司の名前は出力されるけれど、社員の名前は出力されない')
    ...:     Behold('no_employee_name').show(boss)
    ...:
    ...:     print('\n# グローバル変数を参照できるようにする')
    ...:     Behold().show(global_g=g, boss=boss)
    ...:
    ...:     print('\n# 文字列の引数を与えることで、変数の順序を強制する')
    ...:     Behold().show('global_g', 'boss', global_g=g, boss=boss)
    ...:
    ...:     print('\n# 入れ子になっている属性に対しても同様の方法で指定')
    ...:     Behold().show(employee_name=boss.employee.name)
    ...:
    ...: example_func()
    ...:
 # グローバル変数は参照できない
 boss: Item('employee', 'name'), employee: Item('name'), g: None
 
 #上司の名前は出力されるけれど、社員の名前は出力されない
 employee: Item('name'), name: Michael, no_employee_name
 
 # グローバル変数を参照できるようにする
 boss: Item('employee', 'name'), global_g: global_content
 
 # 文字列の引数を与えることで、変数の順序を強制する
 global_g: global_content, boss: Item('employee', 'name')
 
 # 入れ子になっている属性に対しても同様の方法で指定
 employee_name: Toby
 
 In [3]:
 
```

## 結果の保存
Beholdにはグローバルな隠し場所(スタッシュスペース：Stash space)があり、観測結果を保存して後でトップレベルのサマリーに使用することができます。スタッシュスペースはグローバルなので、混乱しないように慎重に管理する必要があります。以下は、stash機能を使ってサマリー情報を出力する例です。 `.get_stash()` 関数で返されるディクショナリーのリストは、Pandas Dataframeのコンストラクタに直接渡すことができるように特別に設計されており、さらなる分析を簡単にすることができます。


```
 In [2]: # %load 07_stash.py
    ...: from pprint import pprint
    ...: from behold import Behold, in_context, get_stash, clear_stash
    ...:
    ...: def my_function():
    ...:     out = []
    ...:     for nn in range(5):
    ...:         x, y, z = nn, 2 * nn, 3 * nn
    ...:         out.append((x, y, z))
    ...:
    ...:         # 変数を隠しておきたい場合は、タグを定義しておく必要があります
    ...:         # タグの名前は、グローバルスタッシュスペースのキーとなります
    ...:         # 次は'test_x'の時にのみ出力されます
    ...:         Behold(tag='test_x').when_context(what='test_x').stash('y', 'z')
    ...:
    ...:
    ...:         # 次は'test_y'のテスト時にのみ出力されます
    ...:         Behold(tag='test_y').when_context(what='test_y').stash('x', 'z')
    ...:
    ...:
    ...:         # 次は'test_z'のテスト時にのみ出力されます
    ...:         Behold(tag='test_z').when_context(what='test_z').stash('x', 'y')
    ...:
    ...:     return out
    ...:
    ...:
    ...: @in_context(what='test_x')
    ...: def test_x():
    ...:     assert(sum([t[0] for t in my_function()]) == 10)
    ...:
    ...: @in_context(what='test_y')
    ...: def test_y():
    ...:     assert(sum([t[1] for t in my_function()]) == 20)
    ...:
    ...: @in_context(what='test_z')
    ...: def test_z():
    ...:     assert(sum([t[2] for t in my_function()]) == 30)
    ...:
    ...: test_x()
    ...: test_y()
    ...: test_z()
    ...:
    ...:
    ...: print('\n# test_x のスタッシュの結果。y と z の値だけを期待している')
    ...: pprint(get_stash('test_x'))
    ...:
    ...: print('\n# test_y のスタッシュの結果。x と z の値だけを期待している')
    ...: pprint(get_stash('test_y'))
    ...:
    ...: print('\n# test_z のスタッシュの結果。x と y の値だけを期待している')
    ...: pprint(get_stash('test_z'))
    ...:
    ...: # 引数がない場合、clear_stash() はすべてのスタッシュを削除されます
    ...: # 名前を指定することで、消去する特定のスタッシュを選択できます
    ...: clear_stash()
    ...:
 
 # test_x のスタッシュの結果。y と z の値だけを期待している
 [{'y': 0, 'z': 0},
  {'y': 2, 'z': 3},
  {'y': 4, 'z': 6},
  {'y': 6, 'z': 9},
  {'y': 8, 'z': 12}]
 
 # test_y のスタッシュの結果。x と z の値だけを期待している
 [{'x': 0, 'z': 0},
  {'x': 1, 'z': 3},
  {'x': 2, 'z': 6},
  {'x': 3, 'z': 9},
  {'x': 4, 'z': 12}]
 
 # test_z のスタッシュの結果。x と y の値だけを期待している
 [{'x': 0, 'y': 0},
  {'x': 1, 'y': 2},
  {'x': 2, 'y': 4},
  {'x': 3, 'y': 6},
  {'x': 4, 'y': 8}]
 
 In [3]:
```



## カスタム属性の抽出
データベースアプリケーションを使用していると、ID番号で参照されているオブジェクトに頻繁に遭遇します。これらのidは、人間が読める情報を抽出するためのレコードキーとして機能します。デバッグの際に、ID番号の羅列でスクリーンダンプされると混乱することがあります。実際に見たいのは、そのidに対応する意味のある名前です。Beholdクラスの1つのメソッドをオーバーライドするだけで、この動作は非常に簡単に実装できます。以下の例はその方法を示しています。


```
 In [2]: # %load 08_custom_attr_extracting.py
    ...: from __future__ import print_function
    ...: from behold import Behold, Item
    ...:
    ...: class CustomBehold(Behold):
    ...:     @classmethod
    ...:     def load_state(cls):
    ...:         cls.name_lookup = {
    ...:             1: 'John',
    ...:             2: 'Paul',
    ...:             3: 'George',
    ...:             4: 'Ringo'
    ...:         }
    ...:         cls.instrument_lookup = {
    ...:             1: 'Rhythm Guitar',
    ...:             2: 'Bass Guitar',
    ...:             3: 'Lead Guitar',
    ...:             4: 'Drums'
    ...:         }
    ...:
    ...:     def extract(self, item, name):
    ...:         """
    ...:         beholdクラスのextract()メソッドをオーバーライドしています
    ...:         このメソッドは、オブジェクトを受け取り、それを文字列に変換します
    ...:
    ...:         デフォルトの動作は、オブジェクトに対して単にstr()を呼び出します
    ...:         """
    ...:         if not hasattr(self.__class__, 'name_lookup'):
    ...:             self.__class__.load_state()
    ...:
    ...:         val = getattr(item, name)
    ...:
    ...:         if isinstance(item, Item) and name == 'name':
    ...:             return self.__class__.name_lookup.get(val, None)
    ...:
    ...:         elif isinstance(item, Item) and name == 'instrument':
    ...:             return self.__class__.instrument_lookup.get(val, None)
    ...:
    ...:         # otherwise, just call the default extractor
    ...:         else:
    ...:             return super(CustomBehold, self).extract(item, name)
    ...:
    ...:
    ...: items = [Item(name=nn, instrument=nn) for nn in range(1, 5)]
    ...:
    ...: print('\n# 標準のBeholdクラスを使ってアイテムを出力')
    ...: for item in items:
    ...:     _ = Behold().show(item)
    ...:
    ...:
    ...: print('\n# CustomBeholdクラスを使用したアイテムを専用エクストラクタで表
    ...: 示する')
    ...: for item in items:
    ...:     _ = CustomBehold().show(item, 'name', 'instrument')
    ...:
 
 # 標準のBeholdクラスを使ってアイテムを出力
 instrument: 1, name: 1
 instrument: 2, name: 2
 instrument: 3, name: 3
 instrument: 4, name: 4
 
 # CustomBeholdクラスを使用したアイテムを専用エクストラクタで出力する
 name: John, instrument: Rhythm Guitar
 name: Paul, instrument: Bass Guitar
 name: George, instrument: Lead Guitar
 name: Ringo, instrument: Drums
 
 In [3]:
 
```

## BeholdのAPI


> **in_context(** context_vars)**
> **context_vars**：コンテキスト変数をキーワード引数で与える

デバッグを実行するための任意のコンテキストを定義することができます。一般的な使用例としては、コードベースのさまざまな場所から呼び出されるコードがあり、特定の場所から呼び出されたときにのみ何が起こるかを知りたい場合があります。その場所をコンテキストで囲み、そのコンテキスト内でのみデバッグすることができます。以下にその例を示します。


```
 In [2]: # %load 20_in_context.py
    ...: from behold import BB  # this is an alias for Behold
    ...: from behold import in_context
    ...:
    ...: def my_function():
    ...:     for nn in range(5):
    ...:         x, y = nn, 2 * nn
    ...:
    ...:         # 'testing' の時だけ出力
    ...:         BB().when_context(what='testing').show('x')
    ...:
    ...:         # 'production' の時だけ出力
    ...:         BB().when_context(what='production').show('y')
    ...:
    ...: # デコレーターを使った'testing' 用コンテキストの設定
    ...: @in_context(what='testing')
    ...: def test_x():
    ...:    my_function()
    ...:
    ...: # テストを実行
    ...: test_x()
    ...:
    ...: # コンテキストマネージャを使用して'production'用のコンテキストを設定し
    ...: with in_context(what='production'):
    ...:    my_function()
    ...:
 x: 0
 x: 1
 x: 2
 x: 3
 x: 4
 y: 0
 y: 2
 y: 4
 y: 6
 y: 8
 
 In [3]:
 
```

>**set_context(**kwargs)**
> **kwargs：**コンテキスト変数をキーワード引数で与える

この機能を使うと、デコレーターやwith文を使わずに、手動でコンテキスト変数を設定することができます。


```
 In [2]: # %load 21_set_context.py
    ...: from behold import Behold
    ...: from behold import set_context, unset_context
    ...:
    ...: set_context(what='my_context')
    ...:
    ...: # コンテキスト変数を出力
    ...: _ = Behold().when_context(what='my_context').show(x='hello')
    ...:
    ...: unset_context('what')
    ...:
 x: hello
 
 In [3]:
 
```


>**unset_context(*keys)**
> **keys：アンセットする**コンテキスト変数の名前を文字列で与える

 `set_context()` と反対の動作で、コンテキスト変数をアンセットする

>**behold.logger.get_stash(name)**
> **name**：取得したい隠し場所（スタッシュ）の名前
> 
>**戻り値**： `behold.stash()` メソッドが呼び出されるたびに、stashされたレコードを保持する辞書のリスト

サンプルコード `07_stash.py` を参照してください。

>**clear_stash(*names)**
>  **name**：クリアしたい隠し場所（スタッシュ）の名前

サンプルコード `07_stash.py` を参照してください。

>**class Behold(tag=None, strict=False, stream=None)**
> **tag**：すべての出力に付けるタグ（デフォルト：なし）
> **strict (Bool)**：  `True` に設定すると、既存のキーのみを `when_contex()` および  `when_values()` メソッドで使用することができます。（デフォルトは `False` )
> **stream (FileObject)** - 書き込みが可能な任意の python ファイルオブジェクト (デフォルト: sys.stdout)

クラス変数
- **stream** ：sys.stdout: 書き込まれるストリーム
- **tag**：出力にタグを付けるための文字列です。デフォルトはなし。
- **strict**： `when_contex()` メソッドと  `when_values()` メソッドで、既存のキーのみを許可するかどうかを設定するブール値です。

Beholdクラスのオブジェクトは、コードベース内の状態を調べるために使用されます。コンソールへの出力をログに記録したり、ステップデバッグ用のエントリポイントをトリガーするために使用できます。

あまりにも頻繁に使用されるため、beholdクラスにはいくつかのエイリアスがあります。次の3つのステートメントは同等です。


```
 from behold import Behold
 from behold import B
 from behold import BB
```

>**Behold.show(*values, **data)**
> **values**：出力したい変数名または属性名のリスト。最大で1つの引数が文字列以外のものになります。
> 文字列は、出力したい変数や属性の名前として解釈されます。文字列以外の引数を1つだけ指定する場合、それは文字列変数で指定された属性を持つオブジェクトでなければなりません。オブジェクトが提供されていない場合、文字列はローカルスコープ内の変数名でなければなりません。
> **data**：キーワード引数のセットです。指定されたキーは、印刷された変数の名前になります。そのキーに関連付けられた値は、そのstr()表現が印刷されます。これらのキーワード引数は、args で渡されたオブジェクトに追加の属性を付加するものと考えることができます。オブジェクトが渡されなかった場合は、これらの kwargs を使用してオブジェクトが作成されます。

このメソッドは、すべてのフィルターに合格した場合は `True` を、そうでない場合は `False` を返します。これにより、必要に応じてデバッグコードで追加のロジックを実行することができます。以下に例を示します。


```
 In [2]: # %load 22_show_returns.py
    ...: from behold import Behold, Item
    ...: a, b = 1, 2
    ...: my_list = [a, b]
    ...:
    ...: # ローカル変数の引数を出力
    ...: Behold().show('a', 'b')
    ...:
    ...: # ローカル変数をキーワード引数で指定して出力
    ...: Behold().show(a=my_list[0], b=my_list[1])
    ...:
    ...: # キーワード引数を使ってローカルス変数の値を出力しますが
    ...: # 指定された順序で出力されるようにする
    ...: Behold().show('b', 'a', a=my_list[0], b=my_list[1])
    ...:
    ...: # オブジェクトの属性値を出力
    ...: item = Item(a=1, b=2)
    ...: Behold().show(item, 'a', 'b')
    ...:
    ...: # show() の戻り値を使って、より多くのデバッグを制御する
    ...: a = 1
    ...: if Behold().when(a > 1).show('a'):
    ...:     import pdb; pdb.set_trace()
    ...:
 a: 1, b: 2
 Out[2]: True
 a: 1, b: 2
 Out[2]: True
 b: 2, a: 1
 Out[2]: True
 a: 1, b: 2
 Out[2]: True
 
 In [3]:
 
```


> **Behold.when(*bools)**
> **bools**：ブール値
 `show()` を有効にするためには、与えたすべてのブール値が  `True` として評価される必要があります。


```
 In [1]: %load 23_when.py
 
 In [2]: # %load 23_when.py
    ...: from behold import Behold
    ...:
    ...: for x in range(10):
    ...:     _ = Behold().when(x == 1).show('x')
    ...:
 x: 1
 
 In [3]:
 
```


> **Behold.when_values(**criteria)**
> **criteria**：var_name=var_valueのキーワード引数
デフォルトでは、Beholdオブジェクトは、出力ストリームに送る前に、すべての変数に対して `str()` を呼び出します。このメソッドを使うと、抽出された文字列表現にフィルターをかけることができます。構文は、 `when_context()` メソッドと全く同じです。以下に例を示します。


```
 In [2]: # %load 24_when_values.py
    ...: from behold import Behold, Item
    ...:
    ...: items = [
    ...:    Item(a=1, b=2),
    ...:    Item(c=3, d=4),
    ...: ]
    ...:
    ...: for item in items:
    ...:    # 内部表現の文字列をフィルター
    ...:    _ = Behold(tag='first').when_values(a='1').show(item)
    ...:
    ...:    # Behold is smart enough to transform your criteria to strings
    ...:    # so this also works
    ...:    # Beholdは、criteriaを文字列に変換するので、次の表記もOK
    ...:    _ = Behold(tag='second').when_values(a=1).show(item)
    ...:
    ...:    # operations.
    ...:    # 変数の内部表現の文字列はローカルスコープには存在しないので、
    ...:    # 論理演算には when_context() と同様な構文を使う必要があります。
    ...:    _ = Behold(tag='third').when_values(a__gte=1).show(item)
    ...:
 a: 1, b: 2, first
 a: 1, b: 2, second
 a: 1, b: 2, third
 
 In [3]:
 
```


> **Behold.when_context(**criteria)**
> **criteria**：var_name=var_valueのキーワード引数

 `when_conext()` メソッドに渡されるキーワード引数は、印刷を行うために満たさなければならないコンテキスト制約を指定することができまう。これらの制約の構文は、 Django のクエリセットに似たものを使用します。印刷が行われるためには、指定されたすべての条件を満たす必要があります。

以下の構文がサポートされています。

-  `x__lt=1` は、 `x < 1` を意味します。
-  `x__lte=1` は  `x <= 1` を意味します。
-  `x__le=1` は、 `x <= 1` を意味します。
-  `x__gt=1` は、 `x > 1` を意味します。
-  `x__gte=1` は  `x >= 1` を意味する
-  `x__ge=1` は  `x >= 1` を意味する
-  `x__ne=1` は  `x != 1 ` を意味する
-  `x__in=[1, 2, 3]` は、 `x in [1, 2, 3]` を意味します。

この構文が必要な理由は、比較されるコンテキスト値がローカルスコープでは利用できないため、通常のPythonの比較演算子は役に立たないためです。


>**Behold.view_context(*context_keys)**
> **context_keys**：コンテキストキーを持つ文字列

 `view_context()` メソッドは、調べているローカル変数と一緒にコンテキスト変数の値を表示することができます。
 `myvar__in=[1, 2] ` のような「in クエリ」でフィルタリングする際に、どのコンテキストがアクティブかを整理するのに便利です。

>**Behold.stash(*values **data)**

stashメソッドは、後で分析するために値を隠しておくことができます。引数は `show()` メソッドと同じです。しかし、 `stash()` メソッドは、出力を書き出す代わりに、出力されるはずだった値をグローバル・リストに入力します。これにより、後でそれらにアクセスできるようになります。


```
 In [2]: # %load 25_stash.py
    ...: from behold import Behold, get_stash
    ...:
    ...: for nn in range(10):
    ...:     # stash()は、タグで作成されたビヨンドオブジェクトに対してのみ実行で
    ...: きます
    ...:     # タグはstashリストのグローバルキーになります
    ...:     behold = Behold(tag='my_stash_key')
    ...:     two_nn = 2 * nn
    ...:
    ...:     _ = behold.stash('nn' 'two_nn')
    ...:
    ...: # これをコードの全く別のファイルで実行します。
    ...: my_stashed_list = get_stash('my_stash_key')
    ...:
 
 In [3]:
 
```

>**Behold.extract(item, name)**
> **item** ：属性を抽出するためのオブジェクトです。. `show()` メソッドにオブジェクトを明示的に提供しなかった場合、Beholdは属性として指定したローカル変数を `Item` オブジェクトに添付します。
> **name**： `item` から抽出する属性名を文字列で与える。

通常はこのメソッドを呼び出す必要はありません。 これは    内部メソッドですが、変数や属性のカスタム抽出ロジックを実装するために公開されている内部メソッドです。このメソッドは、属性を出力用の文字列に変換します。       
デフォルトの実装は次のようになっています。


```
 def extract(self, item, name):
     val = ''
     if hasattr(item, name):
         val = getattr(item, name)
     return str(val)
```

 `Behold` を継承してこのメソッドをオーバーライドすることで 、必要な変換を行うことができます。

例えば、Django のモデル ID を名前に変換するコードは次のようになります。


```
 class CustomBehold(Behold):
     def load_state(self):
         #  辞書を検索するためのロジックをここに書く
         self.lookup = your_lookup_code()
 
     def extract(self, item, name):
         if hasattr(item, name):
             val = getattr(item, name)
             if isinstance(item, Model) and name == 'client_id':
                 return self.lookup.get(val, '')
             else:
                 return super(CustomBehold, self).extract(name, item)
          else:
              return ''
```


>**classbehold.logger.Item(**kwargs)**
> **kwargs**：属性を設定するためのキーワード引数

Itemクラスはは、コンストラクタの引数で属性を設定するシンプルなコンテナクラスです。属性へのアクセスは、オブジェクトと辞書の両方をサポートしています。そのため、たとえば次のような記述がすべてサポートされています。


```
 item = Item(a=1, b=2)
 item['c'] = 2
 a = item['a']
 
```

このクラスのインスタンスは、Beholdオブジェクトでローカル変数の表示を依頼したときに作成されます。表示させたいローカル変数は、Itemオブジェクトの属性として添付されます。
 `05_print_object_attr.py` も参照にてください。



