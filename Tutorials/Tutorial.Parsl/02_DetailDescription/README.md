並列プログラミングライブラリParslを解説
=================
![](https://gyazo.com/a26f39c8503237554724b873d0b49fae.png)

書きかけ...

## Parsl について
Parsl  の名前の由来は Parallel Scripting Library で、文字通りPython で実装された並列処理を行うためのライブラリです。 Parsl を使用すると、Pythonの関数とシェルやコマンドなどの外部コンポーネントで構成される並列プログラムを依存関係で結びつけて非同期・並列のワークフローを作成し実行することができます。ラップトップから共有メモリのマルチコアサーバー、小規模なHPCクラスター、クラウドのKubernetes、スーパーコンピュータまで、あらゆる計算リソースでParslプログラムを実行できるため、容易にスケールアップすることができます。

Parsl は次のような特徴を持っています。

- コードと実行環境の分離：任意の**実行プロバイダ**（PC、クラスター、スーパーコンピュータ、クラウドなど）や**実行モデル**（スレッド、パイロットジョブなど）、エグゼキューター(Slurm、SGE、PBSなど)をサポートするように設計されています
- 暗黙的な並列処理：関数をデコレータでアノテーションするだけで非同期に実行され
- ファイル抽象化：ローカルファイルと同様にリモートファイルを扱うことができる
- データフローモデルのワークフローを定義することができる
- 実行中にワークフローが決定される動的ワークフローを定義できる
- ノートブックやその他のインタラクティブなメカニズムによるインタラクティブな並列プログラミング
- 実行状況のモニタリング

こちらで、[オンラインデモ ](https://mybinder.org/v2/gh/Parsl/parsl-tutorial/master) を使用することができます。

[導入事例 http://parsl-project.org/case_studies.html] で紹介されているように、Parslは様々な科学分野の幅広い研究者に利用されています。


## インストール
parsl は pip コマンドでインストールすることができます。

 bash
```
 $ pip install parsl
```



## Parsl の詳細

## Parslと並行処理
Parslアプリを呼び出すと、メインプログラムや現在実行中の他のタスクと同時に実行される新しいタスクが作成されます。異なるタスクは、実行環境に応じて同じノードや異なるノード、同じコンピュータや異なるコンピュータ上で実行されます。

Parslの実行モデルは、本質的にシーケンシャルであるPythonのネイティブな実行モデルとは異なります。Parslを含まない、あるいは他の同時実行メカニズムを使用しないPythonプログラムは、ステートメントをプログラム内に現れた順に1つずつ実行します。この動作は次の図に示されています。左にPythonプログラム、右にそのプログラムを実行したときに時間の経過とともに実行されるステートメントを上から下に向かって示しています。プログラムが関数を呼び出すたびに，メインプログラム（黒）から関数（赤）へと制御が移ります．関数が戻ってきてからメインプログラムの実行が再開される。




![](https://gyazo.com/ee68dff9f4b112572eda9c8b48381dcc.png)

図1. シーケンシャルでの実行イメージ

これに対して、Parslの実行モデルは本質的にコンカレント（Concurrent:同時処理）です。プログラムがアプリを呼び出すたびに、別の実行スレッドが作成され、メインプログラムは一時停止することなく継続されます。そのため、前述の例は下図のような挙動になります。最初は、メインプログラム（黒）という1つのタスクがあります。 `double()` への最初の呼び出しで2番目のタスク（赤）が、 `double()` への2番目の呼び出しで3番目のタスク（オレンジ）が生成されます。第2タスクと第3タスクは、実行した関数が戻ると終了します。(破線はタスクの開始と終了を表しています)。呼び出されたプログラムは、明示的に指示された場合のみブロック（待機）します。（この場合は `result()` の呼び出しによって）


![](https://gyazo.com/08cd8bb2224026f8ba9851bcf810ee9c.png)

図2. 同時処理での実行イメージ

> **注意**：ここで並列性（Parallelism）ではなく同時性（Concurrency）について述べるのには理由があります。2つのアクティビティが同時に実行できる場合、同時実行となります。2つのアクティビティが同時に実行される場合は、並行して発生します。Parslプログラムが利用可能なプロセッサの数よりも多くのタスクを作成した場合、すべての同時実行アクティビティが並行して実行されるとは限りません。


## Parslと実行
ParslのタスクはPythonのメインプログラムや他のParslのタスクと並行して実行されることを理解してください。次に、これらのタスクがどこでどのように実行されるのかということを考えてみましょう。並列プログラムが実行されるコンピュータの種類を考慮して、Parslでは異なる**エクゼキュータ(parsl.executors)** を使ってタスクを実行することができます。エクゼキュータは、タスクのキューを受け取り、ローカルまたはリモートのリソースで実行する責任があります。

ここでは、Parsl で最もよく使用される 2 つのエクゼキュータについて簡単に説明します。その他のエクゼキュータについては、後で説明することにします。

- **HighThroughputExecutor(HTEX)**：1つまたは複数のプロビジョニングされたノードを使用して、きめ細かなタスク実行を可能にするパイロットジョブモデルを実装しています。HTEXは1つのノード（ラップトップなど）で使用することができ、複数のプロセスを使用して同時実行します。次の図に示すように、HTEXはParslのプロバイダ抽象化（parsl.providers）を使用して、リソースマネージャ（バッチスケジューラやクラウドAPIなど）と通信し、実行期間中にノードのセットをプロビジョニングします（例えば、ParslはSlurmのqsubコマンドを使用して、Slurmクラスタ上のノードを要求します）。HTEXは軽量のワーカーエージェントをノードに配置し、その後メインのParslプロセスに接続します。Parslのタスクは、メインプログラムから接続されたワーカーに送られて実行され、結果は同じメカニズムで返送されます。この方法は、他の方法に比べて多くの利点があります。プログラム全体のために1セットのリソースを取得することで、ジョブスケジューラの長い待ち時間を回避し、個々のノードで多くのタスクをスケジューリングすることができます。


![](https://gyazo.com/c43ae3779be3a2a8aa1325aca0e7722f.png)
図3. HTEXの実行イメージ

- **ThreadPoolExecutor**：ローカルにアクセス可能なスレッドのプールでタスクを実行することができます。実行は同じコンピュータ上で、メインプログラムからフォークされたスレッドプール上で行われるため、タスクは互いにメモリを共有することになります。

## Parslと通信
Parslのタスクは通常、有用な作業を行うために通信を必要とします。Parslでは、パラメータの受け渡しとファイルの受け渡しという2つの形式のコミュニケーションが可能です。次のセクションで説明するように、Parslプログラムは、共有ファイルシステムや環境のサービスと対話することによっても通信することができます。

### パラメータの受け渡し
前述の図２は、パラメータの受け渡しによる通信を示しています。メインプログラムのアプリ `double` を呼び出し `double(3)` は、新しいタスクを作成し、パラメータ値 `3` をその新しいタスクに渡します。タスクの実行が完了すると、その戻り値である `6` がメインプログラムに返されます。同様に、2番目のタスクには値 `5` が渡され、値 `10` が返されます。この場合、渡されるパラメータは単純なint型（整数）ですが、複雑なオブジェクト（Numpy配列、Pandas DataFrames、カスタムオブジェクトなど）をタスクとの間で受け渡しすることもできます。

### ファイルの受け渡し
Parslは、BashアプリとPythonアプリの両方で、ファイルを介した通信をサポートしています。ファイルは、アプリがファイルをサポートするように設計されている場合や、交換するデータが大きい場合、データをPythonオブジェクトに簡単にシリアル化できない場合など、多くの理由でパラメータの受け渡しの代わりに使用されます。Parsl のタスクは共有ファイルシステムを持たないリモートノードで実行される可能性があるため、Parsl は場所に依存しないファイルの参照のために **ファイル抽象化(parsl.data_provider.files.File) 構造**を提供しています。Parsl は、依存するアプリケーションを実行する際に、 `File` オブジェクトをワーカーがアクセス可能なパスに変換します。また、Parsl は複数の方法（FTP、HTTP(S)、Globus、rsync など）を使用して、Parsl アプリ間でファイルを転送することができます。ファイル転送の非同期性に対応するため、Parslはデータの移動をParslアプリのように扱い、実行グラフに依存関係を追加し、転送が完了するのを待ってから依存アプリを実行します。

詳細は「Pythonオブジェクトの受け渡し」で説明しています。

### Futures
パラメータやファイルの受け渡しによる通信には、同期という別の目的もあります。後ほど詳しく解説しますが、Parsl でアプリの呼び出しは 　Futures と呼ばれる特別なオブジェクトを返します。このオブジェクトはアプリが終了するまでの間、特別な未割り当ての状態を持ち、終了した時に戻り値を受け取ります。( `AppFuture` の関数  `result()` は、適用された Futures が値を取るまでブロックします。したがって、メインプログラムの  `print()` は、doubleアプリの呼び出しによって生成された両方の子タスクが戻るまでブロックされます。次の図は、この動作を表しています。前述の図のように上から下ではなく、左から右に時間が進みます。タスク1は、タスク2と3を開始するときに最初はアクティブになり、 `d1.result()` と  `d2.result()` の呼び出しの結果としてブロックされ、それらの値が利用可能になると、再びアクティブになります。


![](https://gyazo.com/f1ea5e38002a7e520d28ac6f3ee814b2.png)


図4. タスクとブロック

## Parsl プログラムと環境
通常のPythonとParslを使用したPython では、コードが実行される「環境」が異なります。ここでいう「環境」とは、変数やモジュール(メモリ環境)、ファイルシステム(ファイルシステム環境)、関数がアクセスできるリソースを指します。

Parslプログラムの動作を理解する上で重要なことは、この新しいタスクが実行される「環境」です。タスクが実行するときの環境は、親タスクや他のタスクと同じなのでしょうか？　異なるメモリ、ファイルシステム、サービス環境を持っているのでしょうか？　その答えは、使用するエクゼキュータと、（ファイルシステム環境の場合は）タスクが実行される場所によって異なります。以下では、 `ThreadPoolExecutor` を除くすべてのParslエグゼキューターを代表する、最も一般的に使用される `HighThroughputExecutor` の動作について説明します。

## メモリ環境
Pythonでは、関数がアクセスできる変数やモジュールはPythonの[スコーピングルール ](https://docs.python.org/ja/3.7/tutorial/classes.html) によって定義されており、関数は関数内で定義された変数（ローカル変数）と関数外で定義された変数（グローバル変数）の両方にアクセスできます。したがって、以下のコードでは、 `print_answer()` 関数の  `print()` がグローバル変数  `answer` にアクセスし、 `"the answer is 42"` と出力されています。



```
 In [2]: # %load 04_random.py
    ...: import random
    ...: factor = 5
    ...:
    ...: def ambiguous_double(x):
    ...:      return x * random.random() * factor
    ...:
    ...: num = ambiguous_double(42)
    ...: print(num)
    ...:
 16.30472534176482
 
 In [3]:
```


```
 In [2]: # %load 02_threadpool_executor.py
    ...: import parsl
    ...: from parsl.app.app import python_app
    ...:
    ...: conf = parsl.load()
    ...:
    ...: answer = 42
    ...:
    ...: @python_app
    ...: def print_answer():
    ...:     print('the answer is', answer)
    ...:
    ...: app = print_answer()
    ...: app.result()
    ...:
 the answer is 42
 
```

 `ThreadPoolExecutor` では問題なく動作します。

 `HighThroughputExecutor` を使用するようにしてみましょう。
これ以降、何度も `HighThroughputExecutor` の設定をすることになるので、コードを簡潔にするために設定をモジュールにしておきます。

 htex_config.py
```
 from parsl.config import Config
 from parsl.providers import LocalProvider
 from parsl.channels import LocalChannel
 from parsl.executors import HighThroughputExecutor
 
 config = Config(
     executors=[
         HighThroughputExecutor(
             label="local_htex",
             cores_per_worker=1,
             max_workers=2,
             provider=LocalProvider(
                 channel=LocalChannel(),
                 init_blocks=1,
                 max_blocks=1,
             ),
         )
     ],
     strategy=None
  )
```



```
 n [2]: # %load 03_htex_executor.py
   ...: import parsl
   ...: from parsl.app.app import python_app
   ...: from htex_config import config
   ...:
   ...: parsl.clear()
   ...: conf = parsl.load(config)
   ...:
   ...: answer = 42
   ...:
   ...: @python_app
   ...: def print_answer():
   ...:     print('the answer is', answer)
   ...:
   ...: app = print_answer()
   ...: app.result()
   ...:
```
　---------------------------------------------------------------------------
　NameError                                 Traceback (most recent call last)
　<ipython-input-2-e8fdd286c410> in <module>
        - 14
        - 15 app = print_answer()
　---> 16 app.result()
　
- (中略)
 
- NameError: name 'answer' is not defined
 
- In [3]:
 


Parslでは `ThreadPoolExecutor` を使用している場合を除き、Parslアプリは、アプリの関数に関連するローカル変数にのみアクセスできる別の環境で実行されます。したがって、上記のプログラムを  `HighThroughputExecutor` で実行した場合は、 `provider_answer()` の  `print()` が値  `42` を割り当てられたグローバル変数  `anser` にアクセスできないため、 `NameError` が発生してしまいます。

同様に、 `import` 文にも同じスコーピング・ルールが適用されるため、以下のプログラムは `ThreadPoolExecutor` ではエラーなく実行されますが、他のエグゼキューターで実行するとエラーが発生します。これは、 `ambiguous_double()` の `return` 文が、関数には知られていない変数（ `factor` ）とモジュール（ `random` ）を参照しているためです。


```
 In [2]: # %load 04_random.py
    ...: import random
    ...: factor = 5
    ...:
    ...: def ambiguous_double(x):
    ...:      return x * random.random() * factor
    ...:
    ...: num = ambiguous_double(42)
    ...: print(num)
    ...:
 46.757888817397664
 
 In [3]:
 
```



```
 In [2]: # %load 05_random_threadpool.py
    ...: import parsl
    ...: from parsl.app.app import python_app
    ...: import random
    ...: factor = 5
    ...:
    ...: conf = parsl.load()
    ...:
    ...: @python_app
    ...: def ambiguous_double(x):
    ...:      return x * random.random() * factor
    ...:
    ...: app = ambiguous_double(42)
    ...: print(app.result())
    ...:
 170.69743451244562
 
 In [3]:
 
```


```
 In [2]: # %load 06_random_htex.py
   ...: import parsl
   ...: from parsl.app.app import python_app
   ...: from htex_config import config
   ...: import random
   ...:
   ...: parsl.clear()
   ...: conf = parsl.load(config)
   ...:
   ...: factor = 5
   ...:
   ...: @python_app
   ...: def ambiguous_double(x):
   ...:      return x * random.random() * factor
   ...:
   ...: app = ambiguous_double(42)
   ...: print(app.result())
   ...:
 ---------------------------------------------------------------------------
 NameError                                 Traceback (most recent call last)
 <ipython-input-2-8d4f8727df64> in <module>
     15
     16 app = ambiguous_double(42)
 ---> 17 print(app.result())
 （中略)
 NameError: name 'random' is not defined
 
 In [3]:
```

このプログラムをすべてのParslワーカーで正しく実行できるようにするには、アプリ内でrandomライブラリをインポートし、factor変数を以下のように引数として渡す必要があります。


```
 In [2]: # %load 07_random_htex_good.py
    ...: import parsl
    ...: from parsl.app.app import python_app
    ...: from htex_config import config
    ...:
    ...: parsl.clear()
    ...: conf = parsl.load(config)
    ...:
    ...: factor = 5
    ...:
    ...: @python_app
    ...: def ambiguous_double(factor, x):
    ...:      import random
    ...:      return x * random.random() * factor
    ...:
    ...: app = ambiguous_double(factor, 42)
    ...: print(app.result())
    ...:
 183.42691370406465
 
 In [3]:
```


## ファイルシステム環境
通常のPythonプログラムでは、Pythonプログラムがアクセスできる環境には、Pythonプログラムが実行されているコンピュータのファイルシステムも含まれます。このため次ののコードでは，カレントディレクトリにあるファイル  `answer.txt` に書き込まれた値を，同じファイルを読むことで取り出すことができ， `print()` で  `the answer is 42` と出力する
ものです。


```
 In [2]: # %load 10_file_env.py
    ...: def print_answer_file():
    ...:     with open('answer.txt','r') as f:
    ...:          print('the answer is',  f.read())
    ...:
    ...: with open('answer.txt','w') as f:
    ...:     f.write('42')
    ...:     f.close()
    ...:
    ...: print_answer_file()
    ...:
 the answer is 42
 
 In [3]:
 
```

Parslアプリがどのファイルシステム環境にアクセスできるかは、そのアプリがどこで実行されるかによって異なります。2つのタスクがファイルシステムを共有するノード上で実行されている場合、それらのタスク（例えば、下図のタスクAとBであり、タスクCではない）はファイルシステム環境を共有しています。したがって、上のプログラムでは、親タスクと子タスクがノード1と2で実行された場合は `the answer is 42` と出力されますが、ノード2と3で実行された場合は出力されません。


![](https://gyazo.com/b7924e3deaec9253790f2868d6ebcc8e.png)

図５．タスクとファイルシステム


## サービス環境
サービス環境とは、RedisサーバやGlobusのデータ管理サービスなど、Parslプログラムからアクセス可能なネットワーク・サービスのことをいいます。これらのサービスはどのタスクからでもアクセス可能です。

## 環境の概要
次にまとめたように、タスクが `ThreadPoolExecutor` で実行された場合は、親タスクのメモリとファイルシステムの環境を共有します。他のエクゼキュータで実行した場合は、独立したメモリ環境を持ち、ファイルシステム環境を他のタスクと共有するかしないかは、タスクの配置場所によって決まります。すべてのタスクは通常、同じネットワークサービスにアクセスできます。


親/他タスクとの共有メモリ
    - Parsl なしの Python       Yes
    - Parsl ThreadPoolExecutor  Yes
    - その他のParslエグゼキューター   No

親タスクとの共有ファイルシステム
    - Parsl なしの Python       Yes
    - Parsl ThreadPoolExecutor  Yes
    - その他のParslエグゼキューター   同じノードで実行した場合OK

他タスクとの共有ファイルシステム
    - Parsl なしの Python       N/A
    - Parsl ThreadPoolExecutor  Yes
    - その他のParslエグゼキューター    同じノードで実行した場合OK

サービス環境を他のタスクと共有
    - Parsl なしの Python       N/A
    - Parsl ThreadPoolExecutor  N/A
    - その他のParslエグゼキューター    N/A


## アプリ
アプリは、Pythonコードや外部のBashシェルコードの断片を表現するためのParslの構造で、非同期的に実行することができます。

Parslのアプリは、Python関数にデコレーターをアノテートする必要があります。

- Pythonアプリ： `@python_app` デコレーターで指定、純粋なPythonコードをカプセル化
- Bashアプリ： `@bash_app` デコレーターで指定、外部アプリケーションやスクリプトの呼び出しをラップ
- Joinアプリ： `@join_app` デコレーターで指定、他のアプリを組み合わせてサブワークフローを形成する


## Pythonアプリ(python_app)
次のコードは、入力値の2倍の値を返すPython関数　 `double(x: int)` を示しています。


```
 In [2]: # %load 20_double.py
    ...: def double(x):
    ...:     return x * 2
    ...:
    ...: a = double(42)
    ...: print(a)
    ...:
 84
 
 In [3]:
```

 `@python_app` デコレーターは、この関数をParsl Pythonアプリとして定義します。


```
 In [2]: # %load 21_double_python_app.py
    ...: import parsl
    ...: from parsl.app.app import python_app
    ...:
    ...: conf = parsl.load()
    ...:
    ...: @python_app
    ...: def double(x):
    ...:     return x * 2
    ...:
    ...: app = double(42)
    ...: print(app.result())
    ...:
 84
 
 In [3]:
```


ParslのPythonアプリは非同期に実行され、リモートで実行される可能性もあるため、関数は共有されたプログラムの状態へのアクセスを前提とすることはできません。例えば、必要なモジュールを明示的にインポートしなければならず、関数の外で使用される変数を参照することはできません。したがって、以下のコードはPythonとしては有効ですが、 `bad_double()` 関数がrandomモジュールを必要とし、外部変数 `` factor `` を参照しているため、Parslとしては有効ではありません。


```
 In [2]: # %load 04_random.py
    ...: import random
    ...: factor = 5
    ...:
    ...: def ambiguous_double(x):
    ...:      return x * random.random() * factor
    ...:
    ...: num = ambiguous_double(42)
    ...: print(num)
    ...:
 137.4516824412887
 
 In [3]:
```

次のようにすることで有効な Parsl コードとすることができます。


```
 # 参照： 07_random_htex_good.py
 factor = 5
 
 @python_app
 def ambiguous_double(factor, x):
      import random
      return x * random.random() * factor
 
 app = ambiguous_double(factor, 42)
 print(app.result())
 
```

Pythonアプリには、プリミティブ型、ファイル、シリアル化可能な複雑な型（numpy配列、scikit-learnモデルなど）を含む、あらゆるPython入力引数を渡すことができます。また、他のParslアプリから返されたParsl Futureが渡されることもあります。この場合、Parslは2つのアプリの間に依存関係を確立し、すべての依存するフューチャーが解決されるまで、依存するアプリを実行しません。

また、Pythonアプリはファイルに作用することもあります。Parsl にこれらのファイルを認識させるためには、次のコードスニペットのように、 `inputs` および/または  `outputs` キーワード引数を使用して、ファイルを指定する必要があります。


```
 In [2]: # %load 23_file_passing_python_app.py
    ...: import os
    ...: import parsl
    ...: from parsl.app.app import python_app
    ...: from parsl.data_provider.files import File
    ...:
    ...: # from parsl.configs.local_threads import config
    ...: from htex_config import config
    ...:
    ...: parsl.clear()
    ...: conf = parsl.load(config)
    ...:
    ...: # 入力ファイルを作成
    ...: cwd = os.getcwd()
    ...: c = open(os.path.join(cwd, 'in.txt'), 'w').write('Hello World!\n')
    ...:
    ...: # Parslの Fileオブジェクトを作成
    ...: infile = File(os.path.join(cwd, 'in.txt'),)
    ...: outfile = File(os.path.join(cwd, 'out.txt'),)
    ...:
    ...: @python_app
    ...: def echo(inputs=[], outputs=[]):
    ...:     with open(inputs[0], 'r') as in_file, open(outputs[0], 'w') as out_f
    ...: ile:
    ...:         out_file.write(in_file.readline())
    ...:
    ...: app = echo(inputs=[infile], outputs=[outfile])
    ...: app.result()
    ...:
 
 In [3]: !cat out.txt
 Hello World!
 
 In [4]:
```


### 特別なキーワード引数
任意のParslアプリ（ `@python_app` または `@bash_app` デコレータで装飾されたPython関数）は、以下の特別な予約キーワード引数を使用できます。

- **inputs(リスト)**： このキーワード引数には、Futures または `File` オブジェクトのリストを定義します。Parslは、アプリを実行する前に、リストアップされた Futuresの結果が解決されるのを待ちます。
- **output: (リスト) **：このキーワード引数は、アプリによって生成される `File` のリストを定義します。このようにリストアップされた各 `File` に対して、Parsl は Futures を作成し、 `File` を追跡し、正しく作成されていることを確認します。この Futuresは、入力引数として他のアプリに渡すことができます。
- **walltime(int)**： このキーワード引数は、アプリの実行時に秒単位で制限をかけます。 `walltime` を超えた場合、Parsl は  `parsl.app.errors.AppTimeout` 例外を発生させます。

### 戻り値
Python アプリは、アプリが実行されたときに返される結果のプロキシとして、 `AppFuture` を返します。この `Futures` はタスクのステータスと結果を待ち、完了したらアプリから返された出力 Python オブジェクトを提示するために使用することができます。エラーやアプリの失敗の場合、Futures は`発生させた例外を保持します。

### 制限事項
アプリに変換可能なPython関数にはいくつかの制限があります。

- 関数は定義された入力引数にのみ作用しなければなりません。つまり、スクリプトレベルの変数やグローバル変数を使用できません。
- 関数は、必要なモジュールを明示的にインポートする必要があります。
- Parslはアプリとの間でPythonオブジェクトをシリアライズするためにcloudpickleとpickleを使用しています。そのため、Parsl はすべての入出力オブジェクトが cloudpickle や pickle でシリアライズできることを要求します。これに失敗すると、 `SerializationError` が発生します。
- Python アプリがリモートで生成した標準出力( STDOUT) と 標準エラー出力(STDERR) はキャプチャされません。


## Bashアプリ
ParslのBashアプリは、外部のアプリケーションやスクリプト、他の言語で書かれたコードを実行するために使われます。Bashアプリは `@bash_app` デコレーターで定義され、関数のボディを形成するPythonコードは、Parslによって実行されるBashシェルのコマンドラインを返さなければなりません。Bashアプリで実行されるBashシェルコードは、任意に長くすることができます。

次のコードスニペットは、Bashアプリ   `echo_hello` の例を示しています。 `echo_hello` は、bashコマンド `'echo "Hello World!"'` を文字列として返します。この文字列はParslによってBashコマンドとして実行されます。


```
 @bash_app
 def echo_hello(stderr='std.err', stdout='std.out'):
     return 'echo "Hello World!"'
 
 # cho_hello()を呼び出すと、シェルコマンドが実行され、
 # "Hello World!"という内容のstd.outファイルが作成されます。
 echo_hello()
 
```

Pythonアプリとは異なり、BashアプリはPythonオブジェクトを返すことができません。代わりに、Bash アプリはファイルを介して他のアプリと通信します。 `@bash_app` でデコレーションされたBashアプリは、入力ファイルと出力ファイルを追跡するために  `inputs` と  `outputs` キーワード引数を受け付けます。ｌ

### 特別なキーワード引数

前述の  `inputs` 、 `ooutputs` 、 `walltime` のキーワード引数に加えて、Bashアプリは以下のキーワードを受け付けます。

- **stdout (string, tuple or parsl.AUTO_LOGNAME)**： 標準出力をリダイレクトするファイルへのパスです。parsl.AUTO_LOGNAMEに設定された場合、ログはタスクIDに応じて自動的に名前が付けられ、実行ディレクトリ(デフォルトでは `runinfo/ジョブ番号` )以下の  `task_logs` の下に保存されます。タプル  `(filename, mode)` に設定された場合、標準出力は指定されたファイルにリダイレクトされ、Python の  `open()` 関数で使用されるように指定されたモードで開かれます。
- **stderr (string or parsl.AUTO_LOGNAME)**：  `stdout` と同様ですが、標準エラー出力用です。
- **label(string) **：アプリが  `stdout=parsl.AUTO_LOGNAME` または  `stderr=parsl.AUTO_LOGNAME` で起動された場合、この引数がログ名に追加されます。

Bashアプリでは、デコレートされた関数に渡された引数から、実行するBashコマンド文字列を構築することができます。


```
 In [2]: # %load 24_bash_app.py
    ...:
    ...: import parsl
    ...: from parsl.app.app import bash_app
    ...:
    ...: conf = parsl.load()
    ...:
    ...: @bash_app
    ...: def echo(arg, inputs=[],
    ...:          stderr=parsl.AUTO_LOGNAME, stdout=parsl.AUTO_LOGNAME):
    ...:     cmdline = f'echo {arg} {inputs[0]} {inputs[1]}'
    ...:     return cmdline
    ...:
    ...: future = echo('Hello', inputs=['World', '!'])
    ...: future.result()     # タスクが完了するまでブロックされる
    ...:
    ...: with open(future.stdout, 'r') as f:
    ...:     msg = f.read()
    ...:     print(msg)
    ...:
 Hello World !
 
 
 In [3]:
 
```


### 戻り値
Bashアプリは、Pythonアプリのように `AppFuture` を返します。この `AppFuture` は、タスクの状態を取得したり、アプリがいつ完了したかを判断したり（例：前のコードフラグメントのように `future.result()` を介して）、例外にアクセスするために使用することができます。Bashアプリは、 `output` 、 `stderr` 、 `stdout` で指定されたファイルを通してのみ結果を返すことができるため、 `AppFuture` が返す値には意味がありません。

BashアプリがUnix終了コード `0` で終了した場合、 `AppFuture` は完了します。他のコードでBashアプリが終了した場合、Parslはこれを失敗として扱い、 `AppFuture` には代わりに `BashExitFailure` 例外が発生します。

### 制限事項
Bashアプリには以下のような制限があります。

- 環境変数はサポートされていません。


## Futures
Pythonプログラムで通常のPython関数が呼び出された場合、Pythonインタープリタは関数の実行完了を待ってから次のステートメントに進みます。しかし、関数が長時間実行されることが予想される場合は、その完了を待たずに、すぐに後続のステートメントの実行を進めることが望ましい場合があります。その場合、関数はその他の計算と同時に実行することができます。

独立したアクティビティを異なるコアやノードで並行して実行することで、並行処理はパフォーマンスの向上につながります。次のコードでは、2つの関数の呼び出しを同時に実行することで、全体の実行時間を短縮できることを示しています。



```
 v1 = expensive_function(1)
 v2 = expensive_function(2)
 result = v1 + v2
 
```

しかし、同時実行には同期の必要性も出てきます。この例では、両方の関数の呼び出しが完了するまで、v1 と v2 の合計を計算することができません。同期は、他のアクティビティ (ここでは  `expensive_function()` の 2 つの呼び出し) が完了するまで、1 つのアクティビティ (ここでは  `result = v1 + v2` というステートメント) の実行をブロックする方法を提供します。

Parslは以下のように同時実行と同期をサポートしています。

- ParslプログラムがParslアプリ（Parslアプリのデコレーターでアノテーションされた関数）を呼び出すと、Parslは新しいタスクを作成し、その関数の結果の代わりにFuturesを直ちに返します。
- その後、プログラムは直ちにプログラム内の次のステートメントに進みます。ある時点で、例えばタスクの依存関係が満たされ、利用可能なコンピューティング能力がある場合、Parslはタスクを実行します。
- タスクが完了すると、Parsl はタスクの出力を含む  Future の値を設定します。

Futures　は、非同期タスクのステータスを追跡するために使用できます。例えば、タスクの作成後、ステータス（実行中、失敗、完了など）、結果へのアクセス、例外の捕捉などを判断するために、Futuresを照会することができます。さらに、Futuresは同期のために使われることもあり、 `result()` メソッドを呼び出したPythonプログラムは　Futuresの実行が完了するまでブロックされます。

Parsl は 2 種類のFuturesを提供します。 `AppFuture` と `DataFuture` です。これらは関連していますが、微妙に異なる並列パターンを可能にします。

## AppFutures
AppFuturesはParslのプログラムを構築するための基本的な構成要素です。Parslアプリのすべての呼び出しは、タスクの実行を監視および管理するために使用できるAppFutureを返します。AppFuturesはPythonのコンカレントライブラリから継承されています。AppFuturesは3つの重要な機能を提供します。

1.  `AppFuture` の  `result()` メソッド
アプリが完了するのを待ち、結果にアクセスするのに使用できます。この関数はブロック化されており、アプリが完了したときまたは失敗したときにのみ返されます。次のコードは、上記の  `expensive_function()` と同様の例を実装したものです。ここでは、sleep_doubleアプリは入力値を単純に2倍にします。このプログラムはsleep_doubleアプリを2回呼び出し、結果の代わりに  `Futures` を返します。この例では、 `Futures` の `result()` メソッドを使って、2回のsleep_doubleアプリの呼び出しの結果が計算されるのを待つ方法を示しています。


```
 In [2]: # %load 30_sleep_double.py
    ...: import parsl
    ...: from parsl.app.app import python_app
    ...: from htex_config import htex_config as config
    ...:
    ...: parsl.clear()
    ...: conf = parsl.load(config)
    ...:
    ...: @python_app
    ...: def sleep_double(x):
    ...:     import time
    ...:     time.sleep(2)
    ...:     return x*2
    ...:
    ...: # doubleed_x1 と doubled_x2 は AppFutures であるため、
    ...: # 同時に2つのsleep_doubleアプリを起動します。
    ...: doubled_x1 = sleep_double(10)
    ...: doubled_x2 = sleep_double(5)
    ...:
    ...: # result()メソッドを呼び出すと、
    ...: # 対応する各アプリの呼び出しが完了するまでブロックされます。
    ...: answer = doubled_x1.result() + doubled_x2.result()
    ...: print(answer)
    ...:
 30
 
 In [3]:
 
```

2.  `AppFuture` の  `done()` メソッド
ブロックすることなく、アプリの状態を確認するために使用することができます。次の例では、 `Future` の  `done()` メソッドを呼び出しても、Pythonのメインプログラムの実行が停止しないことを示しています。



```
 In [2]: # %load 31_done.py
    ...: import parsl
    ...: from parsl.app.app import python_app
    ...: from htex_config import htex_config as config
    ...:
    ...: parsl.clear()
    ...: conf = parsl.load(config)
    ...:
    ...: @python_app
    ...: def sleep_double(x):
    ...:     import time
    ...:     time.sleep(2)
    ...:     return x*2
    ...:
    ...: # doubleed_x1 と doubled_x2 は AppFutures であるため、
    ...: # 同時に2つのsleep_doubleアプリを起動します。
    ...: doubled_x1 = sleep_double(10)
    ...: doubled_x2 = sleep_double(5)
    ...:
    ...: # doubled_x1 の状態をチェックし、
    ...: # 結果が利用可能であればTrueを、そうでなければFalseを出力します。
    ...: print(f'Task 1: {doubled_x1.done()}')
    ...: print(f'Task 2: {doubled_x2.done()}')
    ...: answer = doubled_x1.result() + doubled_x2.result()
    ...:
    ...: print(f'Task 1: {doubled_x1.done()}')
    ...: print(f'Task 2: {doubled_x2.done()}')
    ...: print(answer)
    ...:
 Task 1: False
 Task 2: False
 Task 1: True
 Task 2: True
 30
 
 In [3]:
```


3.  `AppFuture` のプロパティー
 `AppFutures` は、アプリの非同期実行中に発生した例外やエラーを安全に処理する方法を提供します。この例では、Futures の `result()` メソッドを呼び出す際に、標準的なPythonプログラムと同じ方法で例外を捕捉する方法を示しています。


```

 def bad_divide(x):
     return 6/x
 
 # Call bad divide with 0, to cause a divide by zero exception
 doubled_x = bad_divide(0)
 
 # Catch and handle the exception.
 try:
     doubled_x.result()
 except ZeroDivisionError as ze:
     print('Oops! You tried to divide by 0')
 except Exception as e:
     print('Oops! Something really bad happened')
```


Parslでは、特定のアプリで発生した例外を捕捉できるだけでなく、先行する依存アプリの失敗によってアプリが実行できなくなった場合にも  `DependencyErrors` の例外が発生します。つまり、他のアプリが正常に完了することに依存しているアプリは、依存しているアプリのいずれかが失敗すると、 `DependencyErrors` で失敗します。


## DataFutures
 `AppFuture` が非同期アプリの実行を表すのに対し、 `DataFuture` はそのアプリによって生成される `File` を表します。Parslのデータフローモデルでは、依存するアプリ（別のアプリが生成したファイルを消費するアプリ）がいつ実行を開始できるかを判断するために、このような構造が必要になります。

出力としてファイルを生成するアプリを呼び出す場合、Parsl は出力ファイルのリストを (outputs キーワード引数で渡された File オブジェクトのリストとして) 指定する必要があります。Parsl は、アプリが実行されると、各出力ファイルの  `DataFuture` を  `AppFuture` の一部として返します。これらの  `DataFuture` には、 `AppFuture` の  `outputs` プロパティーでアクセスできます。

各  `DataFuture` は、アプリの実行が終了し、対応する `File` が作成されると（指定されていればステージアウトされると）完了します。

 `DataFuture` が後続のアプリの呼び出しに引数として渡されると、後続のアプリは `DataFuture` が完了するまで実行を開始しません。その後、 `inputs` 引数は適切な `File` オブジェクトに置き換えられます。

次のコードスニペットは、 `DataFutures` の使用方法を示しています。この例では、Bashアプリecho の呼び出しで、結果を出力ファイル( `hello1.txt` )に書き込むことを指定しています。メインプログラムは、出力ファイルの状態を（Futures の  `outputs` プロパティーで）確認し、ファイルが作成されるのをブロックで待ちます（ `hello.outputs[0].result()` ）。


```
 # This app echoes the input string to the first file specified in the
 # outputs list
 @bash_app
 def echo(message, outputs=[]):
     return 'echo {} &> {}'.format(message, outputs[0])
 
 # Call echo specifying the output file
 hello = echo('Hello World!', outputs=[File('hello1.txt')])
 
 # The AppFuture's outputs attribute is a list of DataFutures
 print(hello.outputs)
 
 # Print the contents of the output DataFuture when complete
 with open(hello.outputs[0].result(), 'r') as f:
      print(f.read())
```


### Pythonオブジェクトの受け渡し
Parslアプリは、標準的なPython関数のパラメータパスとリターンステートメントを介して通信できます。次の例では、Python の文字列を Parsl アプリに渡したり、Parsl アプリから返したりする方法を示しています。


```
 @python_app
 def example(name):
     return 'hello {0}'.format(name)
 
 r = example('bob')
 print(r.result())
 
```



Parslはcloudpickleとpickleライブラリを使用してPythonオブジェクトをバイト列にシリアライズし、サブミットしたマシンから実行ワーカーまでネットワーク経由で渡すことができます。

そのため、Parslアプリは、ブール値、整数、タプル、リスト、辞書など、Pythonの標準的なデータ型を受け取ったり返したりすることができます。ただし、すべてのオブジェクトがこれらの方法でシリアル化できるわけではありません。クロージャ、ジェネレータ、システムオブジェクトなどのオブジェクトをすべてのエクゼキュータで使用することはできません。

Parsl は、シリアル化できないオブジェクトに遭遇すると  `SerializationError` 例外を発生させます。これは、アプリの引数として渡されたオブジェクトや、アプリから返されたオブジェクトにも当てはまります。
詳細は、「SerializationError の対処」を参照してください。

### データファイルのステージング
Parsl アプリはデータ ファイルを受け取ったり返したりすることができます。ファイルはアプリの `inputs` 引数として渡されたり、実行後にアプリから返されたりします。Parsl は、メインの Parsl プログラム、ワーカー ノード、および外部のデータ ストレージ システム間でファイルを自動的に転送 (ステージング) する機能を提供しています。

入力ファイルは通常の引数として渡すことができますが、アプリの起動時に特別な `inputs` キーワード引数で `File` のリストを指定することもできます。

アプリ内では、 `File` の `filepath` プロパティーを読み取ることで、入力ファイルが実行側のファイルシステムのどこに置かれているかを知ることができます。

出力の `File` オブジェクトも、アプリの起動時に `outputs` パラメータを介して渡される必要があります。この場合、 `File` オブジェクトは、Parsl が実行後に出力を配置する場所を指定します。

アプリ内では、出力の `File` オブジェクトの  `filepath` プロパティーは、対応する出力ファイルが配置されるべきパスを提供し、実行後に Parsl がそれを見つけられるようにします。

アプリからの出力が後続のアプリの入力として使用される場合、出力ファイルが作成されたかどうかを表す `DataFuture` が最初のアプリの `AppFuture` から抽出され、それが2番目のアプリに渡されなければなりません。これにより、後続のアプリに `AppFutures` を渡すことで、アプリが戻ってきたことに基づいて実行順序が決まるのと同じように、アプリの実行が適切に行われます。

Parslプログラムでは、ファイル処理は2つの部分に分かれています。ファイルは `File` オブジェクトを使用して実行場所に依存しない方法で命名され、エクゼキュータはStagingインターフェースのインスタンスを使用してそれらのファイルを実行場所にステージングしたり、実行場所からステージングしたりするように構成されます。

## Parsl のファイル
Parsl はカスタムな `File` オブジェクトを使用して、場所に依存しない方法でファイルを参照およびアクセスします。Parsl の `File` は、URL スキームとファイルへのパスを指定して定義されます。したがって、 `File` は投入側のファイルシステム上の絶対パスを表すこともあれば、外部ファイルへのURLを表すこともあります。

スキームは、ファイルにアクセスするためのプロトコルを定義します。Parslは、 `file` 、 `ftp` 、 `http` 、 `https` 、 `globus` 、 `rsync` の各スキームをサポートしています。スキームが指定されていない場合、Parsl はデフォルトで  `file` スキームを使用します。

次の例では、ローカルでアクセス可能な  `data.txt ` ファイルと、HTTPS でアクセス可能な  `README` ファイルという、異なるスキームの 2 つの `File` を作成しています。


```
 file1 = File('file://home/parsl/data.txt')
 file2 = File('https://github.com/Parsl/parsl/blob/master/README.rst')
 
```

Parslは、ファイルがアクセスされる環境（Parslプログラムやアプリなど）に相対して、ファイルの位置を自動的に変換します。次の例では、そのアプリがどこで実行されるかに関わらず、アプリ内でファイルにアクセスできることを示しています。


```
 @python_app
 def print_file(inputs=[]):
     with open(inputs[0].filepath, 'r') as inp:
         content = inp.read()
         return(content)
 
 # リモートのParsl File を作成
 f = File('https://github.com/Parsl/parsl/blob/master/README.rst')
 
 # Parsl File を与えて print_file アプリを呼び出す
 r = print_file(inputs=[f])
     r.result()
```

このファイルの転送方法は、Parslの設定で指定されたスキームとステージング・プロバイダーによって異なります。

## ステージングプロバイダー
Parsl は、ワーカーにステージングインスタンスのリストを指定することで、ファイルが存在している場所と実行場所の間で透過的にファイルをステージングすることができます。これらのステージング インスタンスは、実行場所でのファイルの転送方法を定義します。このリストは、エクゼキュータが構築される際に storage_access パラメータとして指定する必要があります。

Parsl には、上記で定義されたスキームを使ってファイルを移動するための、いくつかのステージング プロバイダが含まれています。デフォルトでは、Parsl の実行ファイルは、ローカルおよび共有ファイルシステム用の  `NoOpFileStaging` プロバイダと、リモートのストレージとの間でファイルを転送するための HTTP(S) および FTP のステージング プロバイダという、3 つの一般的なステージング プロバイダとともに作成されます。次の例では、デフォルトのステージング・プロバイダを明示的に設定する方法を示しています。


```
 from parsl.config import Config
 from parsl.executors import HighThroughputExecutor
 from parsl.data_provider.data_manager import default_staging
 
 config = Config(
     executors=[
         HighThroughputExecutor(
             storage_access=default_staging,
             # 指定した順に評価される
             # storage_access=[NoOpFileStaging(), FTPSeparateTaskStaging(), HTTPSeparateTaskStaging()],
         )
     ]
 )
```


Parsl は、ファイルを必要としたり生成したりするアプリの呼び出しに対して、ステージングがいつ発生するかをさらに区別しています。ステージングは、アプリの実行前に、実行中のタスクと一緒に行われる場合（タスク内ステージング(in-Task Staging)）と、別のタスクとして行われる場合（別タスクステージング）があります。In-task staging は、Parsl タスクの周りで実行されるラッパーを使用するため、タスクが実行されるリソース上で発生します。別タスクのステージングでは、新しいParslタスクをグラフに挿入し、ステージングタスクとそのファイルに依存するタスクの間に依存関係を関連付けます。別タスクのステージングは、投入側（Globusを使用する場合など）でも実行側（HTTPS、FTPなど）でも発生します。

### ローカル/共有ファイルシステムでのNoOpFileStaging
 `NoOpFileStaging` プロバイダは、パスまたはファイルURLスキームで指定されたファイルが、送信側と実行側の両方で利用可能であることを前提としています。これは、たとえば、共有ファイルシステムがある場合に発生します。この場合、ファイルは移動せず、 `File` オブジェクトは、Parslプログラムと実行中のタスクに同じファイルパスを提示するだけです。

以下のように定義されたファイルは、 `NoOpFileStaging` プロバイダによって処理されます。



```
 file1 = File('file://home/parsl/data.txt')
 file@ = File('/home/parsl/data.txt')
```

 `NoOpFileStaging` プロバイダは、すべてのエクゼキュータでデフォルトで有効になっています。以下のように、明示的に唯一のステージング・プロバイダーとして設定することができます。


```
 from parsl.config import Config
 from parsl.executors import HighThroughputExecutor
 from parsl.data_provider.file_noop import NoOpFileStaging
 
 config = Config(
     executors=[
         HighThroughputExecutor(
             storage_access=[NoOpFileStaging()]
         )
     ]
 )
```


### FTP、HTTP、HTTPS：個別タスクのステージング
ftp、http、httpsのURLスキームで指定されたファイルは、HTTP GETまたはanonymous FTPコマンドを使ってステージングされます。これらのコマンドは、個別のParslタスクとして実行され、対応するアプリが実行される前に完了します。これらのプロバイダは、出力ファイルのステージアウトには使用できません。

次の例では、リモートの FTP サーバーでアクセス可能なファイルを定義しています。




## 参考
- [Parsl オフィシャルサイト ](https://parsl-project.org/)
- [並列プログラミングライブラリParslの紹介]


#パイプライン処理
#ワークフローツール


