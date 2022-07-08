Pypelnを使って効率良くデータを操作してみよう
=================

# はじめに
この使用は Pypelin をつかったパイプライ処理について説明したものです。

# Pypeln について
[Pypeln ](https://cgarciae.github.io/pypeln/) (発音は pypeline - パイプライン) は、並列データパイプラインを作成するためのシンプルで強力なPythonライブラリです。

主な機能には次のものがあります。
  - **シンプル**　ー　Pypelnは、SparkやDaskのようなフレームワークでは大げさで不自然に感じられる、並列性と並行性を必要とする中規模のデータタスクを解決するために設計されています。
  - **使いやすい** ー　Pypelnは、通常のPythonコードと互換性のある、使い慣れた関数型APIを提供しています。
  - **柔軟** ー　Pypelnは、全く同じAPIでProcesses、Threads、asyncio.Tasksを使ったパイプラインを構築できます。
  - **きめ細かな制御** ー　Pypelnでは、パイプラインの各段階で使用されるメモリとCPUのリソースを制御できます。



# インストール
Pypeln のインストールは次のように行います。

 bash
```
 # Linux or MacOS
 $ python -m pip install pypeln
 
 # Windows
 $ py -3 -m pip install pypeln
```


## アーキテクチャ
![](https://gyazo.com/6c62fc8246ad2dc31a31bad9c1489b23.png)
複数の同時進行ステージで構成される各**ステージ(Stage)** には、タスクを実行する1つ以上の**ワーカー(Worker)**が含まれます。
関連するステージは**キュー(Queue)** で結ばれていて、あるステージのワーカーはキューにアイテムを入れ、他のステージのワーカーはキューからアイテムを取得します。
ソースステージはイテラブルオブジェクトを格納し、後続のシンクステージ(Sink Srage)は、それをイテラブルオブジェクトとして取り出すことができます。


### ステージの種類
Pypelnには3種類のステージがあり、各ステージには関連するワーカーとキューのタイプがあります。
ステージの種類と使用されるモジュールの関係は次のようになっています。

 Pypeln のステージタイプ

| テージタイプ  | ワーカー | キュー |
|:--|:--|:--|
| pl.process.Stage | multiprocessing.Process | multiprocessing.Queue |
| pl.thread.Stage | threading.Thread | queue.Queue |
| pl.task.Stage | asyncio.Task | asyncio.Queue |

使用するステージの種類によって、メモリ管理、並行処理、ステージ間通信のオーバーヘッド、ワーカーの初期化オーバーヘッドなどの特徴が異なります。

 pypeln のステージ別の特徴

| ステージ | メモリ空間 | 同時実行 | 並列    | 通信オーバヘッド  | 初期化オーバーヘッド |
|:--|:--|:--|:--|:--|:--|
| process  | 独立 | cpu + I/O処理     | cpu + I/O書折     | 高    |  高 |
| thread   | 共有 | I/O処理   | I/O処理   | なし     | 中 |
| task     | 共有 | I/O最適化     | I/O最適化     | なし    | 低 |

### ステージ
ステージは、計算に関するメタ情報のみを含むイテラブルオブジェクトです。パイプラインを実際に実行するには、forループ、リスト呼び出し、 `pl.<module>.run` などを使用して反復します。


```
 In [2]: # %load c00_stage.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_add1(x):
    ...:     time.sleep(random()) # <= 遅い計算処理を想定...
    ...:     return x + 1
    ...:
    ...: data = range(10)  # [0, 1, 2, ..., 9]
    ...: stage = pl.thread.map(slow_add1, data, workers=3, maxsize=4)
    ...:
    ...: for x in stage:
    ...:     print(x)      # e.g. 2, 1, 5, 6, 3, 4, 7, 8, 9, 10
    ...:
 1
 2
 5
 4
 7
 6
 9
 10
 3
 8
 
 In [3]:
 
```

この例では `pl.thread` を使用していますが、他のすべてのモジュールでも同じように動作します。pypelnはイテラブルのAPIインターフェースを実装しているので、非常に直感的に使用でき、他のほとんどのpythonコードと互換性があります。

### ワーカー
各ステージはいくつかのワーカーを定義し、それらは通常pypelnの様々な関数の `workers` 引数で制御することができます。基本的には、実行するマシンのコア数より多くのワーカーを作らないようにしましょう。リソースの奪い合いになるため性能が低下してしまいます。

画像処理、データ変換など、重いCPU処理を並列で行う必要がある場合に、Process を使用します。プロセスをフォークすると、すべてのメモリが新しいプロセスにコピーされ、初期化が遅くなり、プロセス間通信はpythonオブジェクトをシリアライズする必要があるためコストがかかります。しかし、実質的にGILから逃れることができるので、真の並列性を得ることができます。
Threadは、OSや非同期APIを公開していないライブラリとのやりとりのような、同期的なIOタスクに非常に適しています。
Taskは非同期IO操作に高度に最適化されており、通常のPythonオブジェクトなので作成時のコストが非常に低く、イベントループが効率的に管理してくれるので、コア数より多く作成することができます。

### キュー
ワーカー同士はQueueを通じて通信します。各Queueが保持できる最大要素数は、pypelnの様々な関数の `maxsize` 引数で制御されます。この値のデフォルトはは0で、要素数に制限はありません。しかし、 `maxsize` が設定されると、キューがいっぱいになった（ `maxsize` で指定した数値に達した）ときに前のステージが新しい要素をキューに押し込むのを防ぐメカニズムとして機能します。

プロセス間の通信は、pythonオブジェクトをシリアライズする必要があるため、コストがかかります。これは、numpy配列やバイナリオブジェクトなどの大きなオブジェクトを渡すときにかなりのオーバーヘッドとなります。このオーバーヘッドを避けるために、プロセス間でファイルパスのようなメタデータ情報のみを渡すようにします。
スレッドやタスク間の通信にはオーバーヘッドがありません。すべてがメモリ内で行われるため、シリアライズのオーバーヘッドもありません。

### リソースの管理
リソースオブジェクト (例えば http やデータベースセッション) を作成する必要がある場合、 効率化のために)各ワーカーが生きている間中ずっと続くことが期待される場合が多々あります。そのようなオブジェクトのライフサイクルをサポートし、効果的に管理するために、pypelnの関数のほとんどは  `on_start` と  `on_done` コールバックを受け付けます。

ワーカーが作成されると、その `on_start` 関数が呼び出されます。この関数はリソースオブジェクトを含む辞書を返すことができ、与えた関数( `f` 引数か第1引数)と  `on_done` 引数に与えた関数を使用することができます。たとえば、次のようになります。


```
 import pypeln as pl
 
 def on_start():
     return dict(
         http_session = get_http_session(),
         db_session = get_db_session(),
     )
 
 def func(x, http_session, db_session):
     # 何かしらの処理
     return v
 
 def on_done(http_session, db_session):
     http_session.close()
     db_session.close()
 
 
 stage = pl.process.map(func, stage, workers=3, on_start=on_start, on_done=on_done)
 
```

### 特殊な引数
依存性を関数に適用させるために特殊な引数を受け取ります。

-  `worker_info` ー　引数`f `、` on_start`、 `on_done` は  `worker_info` 引数を定義することができます。 Worker に関する情報を持つオブジェクトが渡されます。
-  `stage_status` ー　 `on_done` は、 `stage_status` 引数を定義することができます。
-  `element_index` ー　与えた関数(引数 `f` もしくは第1引数) には要素のインデックスを表すタプルを渡すことができます。このインデックスは、オリジナル/ソースのイテラブル上での要素の作成順序を表し、順序付き操作が実装される基礎となるメカニズムです。通常、これは単一の要素のタプルになりますが、 flat_map のような操作では、順序を適切に追跡するためにインデックスの次元が追加されます。



# 動作モード
## プロセス
processモジュールを使用することで、multiprocessing.Processワーカーをベースとしたパイプラインを作成することができます。

 c01_process.py
```
 import pypeln as pl
 import time
 from random import random
 
 def slow_add1(x):
     time.sleep(random()) # <= some slow computation
     return x + 1
 
 def slow_gt3(x):
     time.sleep(random()) # <= some slow computation
     return x > 3
 
 
 def main():
     data = range(10) # [0, 1, 2, ..., 9]
 
     stage = pl.process.map(slow_add1, data, workers=3, maxsize=4)
     stage = pl.process.filter(slow_gt3, stage, workers=2)
 
     data = list(stage) # e.g. [8, 6, 9, 4, 8, 10, 7]
     print(data)
 
 if __name__ == '__main__':
     main()
     
```

 bash
```
 $ python c01_process.py
 [5, 4, 6, 8, 10, 7, 9]
 
```

各ステージで、ワーカーの数を指定することができます。 `maxsize` 引数は、ステージが同時に保持できる要素の最大量を制限します。

## multiprocessing モジュールの制約
multiprocessingモジュールは、IPythonで使用する場合、次のような大きな制約があります。

> 注釈 このパッケージに含まれる機能を使用するためには、子プロセスから __main__ モジュールをインポートできる必要があります。このことについては プログラミングガイドライン で触れていますが、ここであらためて強調しておきます。なぜかというと、いくつかのサンプルコード、例えば multiprocessing.pool.Pool のサンプルはインタラクティブシェル上では動作しないからです。[Python 公式ドキュメント multiprocessing ](https://docs.python.org/ja/3/library/multiprocessing.html)


## スレッド
threadモジュールを使用することで、threading.Thread ワーカーに基づいたパイプラインを作成することができます。


```
 In [2]: # %load c02_thread.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_add1(x):
    ...:     time.sleep(random()) # <= some slow computation
    ...:     return x + 1
    ...:
    ...: def slow_gt3(x):
    ...:     time.sleep(random()) # <= some slow computation
    ...:     return x > 3
    ...:
    ...:
    ...: def main():
    ...:     data = range(10) # [0, 1, 2, ..., 9]
    ...:
    ...:     stage = pl.thread.map(slow_add1, data, workers=3, maxsize=4)
    ...:     stage = pl.thread.filter(slow_gt3, stage, workers=2)
    ...:
    ...:     data = list(stage) # e.g. [8, 6, 9, 4, 8, 10, 7]
    ...:     print(data)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [4, 7, 5, 9, 6, 10, 8]
 
 In [3]:
```

このコードでは、ワーカーがスレッドであることを除いて、プロセスの場合とまったく同じになります。

## タスク
taskモジュールを使うことで、asyncio.Taskワーカーをベースにしたパイプラインを作成することができます。


```
 In [2]: # %load c03_task.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_add1(x):
    ...:     time.sleep(random()) # <= some slow computation
    ...:     return x + 1
    ...:
    ...: def slow_gt3(x):
    ...:     time.sleep(random()) # <= some slow computation
    ...:     return x > 3
    ...:
    ...:
    ...: def main():
    ...:     data = range(10) # [0, 1, 2, ..., 9]
    ...:
    ...:     stage = pl.task.map(slow_add1, data, workers=3, maxsize=4)
    ...:     stage = pl.task.filter(slow_gt3, stage, workers=2)
    ...:
    ...:     data = list(stage) # e.g. [8, 6, 9, 4, 8, 10, 7]
    ...:     print(data)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [4, 5, 6, 7, 8, 9, 10]
 
 In [3]:
 
```

タスクは概念的にはスレッドに似ていますが、すべてがシングルスレッドで実行され、タスクワーカーは動的に作成されます。もしコードが非同期タスクの中で実行されているなら、ブロックを避けるためにステージ上でawaitを使用することができます。

 ppython
```
 In [2]: # %load c04_task_await.py
    ...: import pypeln as pl
    ...: import asyncio
    ...: from random import random
    ...:
    ...: async def slow_add1(x):
    ...:     await asyncio.sleep(random()) # <= some slow computation
    ...:     return x + 1
    ...:
    ...: async def slow_gt3(x):
    ...:     await asyncio.sleep(random()) # <= some slow computation
    ...:     return x > 3
    ...:
    ...:
    ...: async def main():
    ...:     data = range(10) # [0, 1, 2, ..., 9]
    ...:
    ...:     stage = pl.task.map(slow_add1, data, workers=3, maxsize=4)
    ...:     stage = pl.task.filter(slow_gt3, stage, workers=2)
    ...:
    ...:     data = await stage # e.g. [5, 6, 9, 4, 8, 10, 7]
    ...:     print(data)
    ...:
    ...:
    ...: if __name__ == '__main__':
    ...:     asyncio.run(main())
    ...:
 [5, 4, 9, 6, 7, 8, 10]
 
 In [3]:
 
```

 `await` は  `async` として宣言された関数の内部でしか使用できないことに注意してください。

## 同期（Sync)
syncモジュールは、同期ジェネレータを使用したすべての操作を実装しています。このモジュールは、デバッグや、重いCPUやIOタスクを実行する必要はないが、 `pl.*.ordered` のような特定の関数が依存する要素の順序情報を保持したい場合に便利です。


```
 In [2]: # %load c05_sync.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_add1(x):
    ...:     return x + 1
    ...:
    ...: def slow_gt3(x):
    ...:     return x > 3
    ...:
    ...: def main():
    ...:     data = range(10) # [0, 1, 2, ..., 9]
    ...:
    ...:     stage = pl.sync.map(slow_add1, data, workers=3, maxsize=4)
    ...:     stage = pl.sync.filter(slow_gt3, stage, workers=2)
    ...:
    ...:     data = list(stage) # [4, 5, 6, 7, 8, 9, 10]
    ...:     print(data)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [4, 5, 6, 7, 8, 9, 10]
 
 In [3]:
 
```

 `workers` や  `maxsize` のような引数は、API 互換性のためにこのモジュールの関数で受け入れられますが、無視されます。

## 混合パイプライン
異なるワーカータイプを使用してパイプラインを作成し、それぞれのタイプが与えられたタスクに最適であるようにすることで、コードから最大のパフォーマンスを得ることができます。


```
 data = get_iterable()
 data = pl.task.map(f1, data, workers=100)
 data = pl.thread.flat_map(f2, data, workers=10)
 data = filter(f3, data)
 data = pl.process.map(f4, data, workers=5, maxsize=200)
```

ステージはイテラブルオブジェクトなので、PypelnはどんなPythonのコードにもスムーズに統合されますが、各ステージがどのように動作するかには注意する必要があります。

# パイプ演算子
ほとんどの関数は、 `stage` 引数が与えられない場合、 `stage` の代わりに `partial` を返すことができるようになっています。これらのPartialは，足りない `stage` 引数を受け取って計算を呼び出すcallableです。この仕組みにより、次の2つの式は等価となります。


```
 pl.process.map(f, stage, **kwargs)
```


```
 pl.process.map(f, **kwargs)(stage)
```

Partial は、パイプ演算子（ `|` ）を次のように実装しています。


```
 x | partial
```


```
 partial(x)
```

これにより、Pypeln では、パイプ演算子( `|` )を使用してパイプラインを作成することができます。


```
 In [2]: # %load c06_pipe.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_add1(x):
    ...:     time.sleep(random()) # <= some slow computation
    ...:     return x + 1
    ...:
    ...: def slow_gt3(x):
    ...:     time.sleep(random()) # <= some slow computation
    ...:     return x > 3
    ...:
    ...:
    ...: def main():
    ...:     data = (
    ...:             range(10)
    ...:             | pl.thread.map(slow_add1, workers=3, maxsize=4)
    ...:             | pl.thread.filter(slow_gt3, workers=2)
    ...:             | list
    ...:         )
    ...:     print(data)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 
 [4, 6, 8, 9, 5, 10, 7]
 
 In [3]:
```

# API
ステージタイプごとに同じ関数が用意されていて。問題の用途に応じたステージを選べるようになっています。

  -  `concat` ー各ステージの要素を順次追加し、複数のステージを1つのステージに連結／統合する（順序は保持しない）
  -  `each` ーデータ中の各要素に対して関数 `f` を実行しますが、ステージ自体は要素を生成しないステージを作成する
  -  `filter` ー　組み込み `filter` 関数のように振る舞いますが、並行処理が追加されている
  -  `flat_map` ー 引数 `f` (あるいは第1引数）に与えた関数をデータ上にマッピングするステージを作成する
  -  `from_iterable` -ーイテラブルからステージを作成する
  -  `map` ーデータ上に関数 `f` をマッピングするステージを作成する
  -  `ordered` ーパイプラインのソース iterable (複数可) で作成された順序に基づいて要素をソートするステージを作成する
  -  `run` ー　1つまたは複数のステージを、そのイテレータが要素を使い果たすまで繰り返し処理する
  -  `to_iterable` ーステージからイテラブルを作成する


## pl.process API
processモジュールを使用すると、Pythonのmultiprocessingモジュールを使用して、Pypelnの一般的なアーキテクチャに従ってパイプラインを作成することができます。このモジュールは、CPU負荷の高い処理で真の並列性が必要な場合に使用します。プロセス生成時のコストも高いため使用する用途を十分に検討してください。

このモジュールのほとんどの関数は、通常のPythonコードとシームレスに組み合わせることができるイテラブルインターフェイスを実装した  `pl.process.Stage` オブジェクトを返します。

## pl.thread API
\threadモジュールを使用すると、threadingモジュールのオブジェクトを使用して、Pypelnの一般的なアーキテクチャに応じたパイプラインを作成することができます。このモジュールは、同期的な IO 操作を行う必要があり、重い CPU 操作を行う必要がない場合に使用します。

このモジュールのほとんどの関数は、通常のPythonコードとシームレスに組み合わせることができるイテラブルインタフェースを実装した  `pl.thread.Stage` オブジェクトを返します。


## pl.task API
taskモジュールを使うと、asyncioモジュールを使って、Pypelnの一般的なアーキテクチャに従ったパイプラインを作成することができます。効率的な非同期 I/O 操作を実行する必要があり、重い CPU 操作を実行する必要がない場合に、このtaskモジュールを使用します。

このモジュールのほとんどの関数は、Iterable、AsyncIterable、Awaitableインターフェースを実装した `pl.task.Stage` オブジェクトを返すので、通常のPythonコードとシームレスに結合することができます。


## pl.sync API
sync モジュールは他のモジュールと同じ API に従っていますが、通常の Python ジェネレータを使用して同期的にコードを実行します。重いCPUやIOタスクを実行する必要はないけれど、 `pl.*.ordered` のような特定の関数が依存する要素の順序情報を保持したい場合に、このモジュールからの関数を使用してください。

 `workers` や  `maxsize` のような一般的な引数は、API 互換性のためにこのモジュールの関数で受け入れられますが、無視されます。

このモジュールのほとんどの関数は、通常の Python コードとシームレスに組み合わせることを可能にする通常の Iterable インターフェイスである  `pl.sync.Stage` を返します。


## concat()

各ステージの要素を順次追加していくことで、多くのステージを1つのステージに連結／統合します（順序は保持されません）。


```
 pl.process.concat(stages: List[Union[pypeln.process.stage.Stage[~A], Iterable[~A]]], maxsize: int = 0) -> pypeln.process.stage.Stage
```

python
```
 pl.thread.oncat(stages: List[Union[pypeln.thread.stage.Stage[~A], Iterable[~A]]], maxsize: int = 0) -> pypeln.thread.stage.Stage
```


```
 pl.task.concat(stages: List[Union[pypeln.task.stage.Stage[~A], Iterable[~A], AsyncIterable[~A]]], maxsize: int = 0) -> pypeln.task.stage.Stage
```


```
 pl.sync.concat(stages: List[Union[pypeln.sync.stage.Stage[~A], Iterable[~A]]], maxsize: int = 0) -> pypeln.sync.stage.Stage
```

- **引数**
  -  `stages` ー　ステージのリスト、もしくはイテラブル
  -  `maxsize` ー ステージが同時に保持できるオブジェクトの最大数です。 `0` (デフォルト) に設定すると、ステージは無制限に成長することができます。syncモジュールではAPI互換性のために受け入れますが、無視されます。
- 戻り値
  - Stageオブジェクト

 c10_process_concat.py
```
 import pypeln as pl
 
 stage_1 = [1, 2, 3]
 stage_2 = [4, 5, 6, 7]
 
 
 def main():
     stage_3 = pl.process.concat([stage_1, stage_2])
     for d in stage_3:
         print(d)
 
 if __name__ == '__main__':
     main()
```

 bash
```
 $ python c10_process_concat.py
 1
 4
 2
 3
 5
 6
 7
 
```



```
 In [2]: # %load c20_thread_concat.py
    ...: import pypeln as pl
    ...:
    ...: stage_1 = [1, 2, 3]
    ...: stage_2 = [4, 5, 6, 7]
    ...:
    ...:
    ...: def main():
    ...:     stage_3 = pl.thread.concat([stage_1, stage_2])
    ...:     for d in stage_3:
    ...:         print(d)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 1
 2
 3
 4
 5
 6
 7
 
 In [3]:
```



```
 In [2]: # %load c30_task_concat.py
    ...: import pypeln as pl
    ...:
    ...: stage_1 = [1, 2, 3]
    ...: stage_2 = [4, 5, 6, 7]
    ...:
    ...:
    ...: def main():
    ...:     stage_3 = pl.task.concat([stage_1, stage_2])
    ...:     data = list(stage_3)
    ...:     print(data)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [1, 2, 3, 4, 5, 6, 7]
 
 In [3]:
 
```




```
 In [2]: # %load c40_task_concat.py
    ...: import pypeln as pl
    ...:
    ...: stage_1 = [1, 2, 3]
    ...: stage_2 = [4, 5, 6, 7]
    ...:
    ...:
    ...: def main():
    ...:     stage_3 = pl.sync.concat([stage_1, stage_2])
    ...:     data = list(stage_3)
    ...:     print(data)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [1, 4, 2, 5, 3, 6, 7]
 
 In [3]:
 
```



## each()
データ中の各要素に対して関数 `f` を実行しますが、ステージ自体は要素を生成しないステージを作成します。ディスクへの書き込み、データベースへの保存など、特定のアクションを実行し、結果を生成しないシンクステージに使用されます。


```
 pl.process.each(f: pypeln.process.api.each.EachFn, stage: Union[pypeln.process.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, workers: int = 1, maxsize: int = 0, timeout: float = 0, on_start: Callable = None, on_done: Callable = None, run: bool = False) -> Union[pypeln.process.stage.Stage[~B], NoneType, pypeln.utils.Partial[Optional[pypeln.process.stage.Stage[~B]]]]
```


```
 pl.thread.each(f: pypeln.thread.api.each.EachFn, stage: Union[pypeln.thread.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, workers: int = 1, maxsize: int = 0, timeout: float = 0, on_start: Callable = None, on_done: Callable = None, run: bool = False) -> Union[pypeln.thread.stage.Stage[None], NoneType, pypeln.utils.Partial[Optional[pypeln.thread.stage.Stage[None]]]]
```


```
 pl.task.each(f: pypeln.task.api.each.EachFn, stage: Union[pypeln.task.stage.Stage[~A], Iterable[~A], AsyncIterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, workers: int = 1, maxsize: int = 0, timeout: float = 0, on_start: Callable = None, on_done: Callable = None, run: bool = False) -> Union[pypeln.task.stage.Stage[~B], NoneType, pypeln.utils.Partial[Optional[pypeln.task.stage.Stage[~B]]]]
```


```
 pl.sync.each(f: pypeln.sync.api.each.EachFn, stage: Union[pypeln.sync.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, workers: int = 1, maxsize: int = 0, timeout: float = 0, on_start: Callable = None, on_done: Callable = None, run: bool = False) -> Union[pypeln.sync.stage.Stage[None], NoneType, pypeln.utils.Partial[Optional[pypeln.sync.stage.Stage[None]]]]
```

- 引数
  -  `f` ー  `f(x) -> None` のシグニチャを持つ関数
  -  `stage` ー ステージもしくはイテラブル
  -  `workers` ー　ステージで保持するワーカーの数。syncモジュールではAPI互換のために受け入れますが、無視されます。
  -  `maxsize` 　ー　ステージが同時に保持できるオブジェクトの最大数です。 `0` (デフォルト) に設定すると、ステージは	無制限に成長することができます。syncモジュールではAPI互換のために受け入れますが、無視されます。
  -  `timeout` 　ー 現在のタスクがまだ完了していない場合、ワーカーを停止させるまでの秒数。デフォルトは  `0` で、これは無制限を意味します。
  -  `on_start` ー  `on_start(worker_info) -> kwargs` のシグニチャを持つ関数を与えます。 `kwargs` には、 `f` と `on_done` に与えるキーワード引数  `dict` を指定することができます。
  -  `on_done` ー　 `on_done(stage_status)` のシグニチャをもつ関数を与えます。この関数は、ワーカーが終了したときに、ワーカーごとに一度だけ実行されます。
- 戻り値
  - もし  `stage` 引数が与えられていなければ、この関数は  `Partial` を返します。もし  `run=False` (default) ならば新しいステージを返し、もし  `run=True` ならばステージを実行し  `None` を返します。



 c11_process_each.py
```
 import pypeln as pl
 
 def process_image(image_path):
     image = load_image(image_path)
     image = transform_image(image)
     save_image(image_path, image)
 
 files_paths = get_file_paths()
 stage = pl.process.each(process_image, file_paths, workers=4)
 pl.process.run(stage)
 
```


 c21_thread_each.py
```
 import pypeln as pl
 
 def process_image(image_path):
     image = load_image(image_path)
     image = transform_image(image)
     save_image(image_path, image)
 
 files_paths = get_file_paths()
 stage = pl.thread.each(process_image, file_paths, workers=4)
 pl.process.run(stage)
 
```


 c31_tasaks_each.py
```
 import pypeln as pl
 
 def process_image(image_path):
     image = load_image(image_path)
     image = transform_image(image)
     save_image(image_path, image)
 
 files_paths = get_file_paths()
 stage = pl.task.each(process_image, file_paths, workers=4)
 pl.process.run(stage)
 
```


 c31_sync_each.py
```
 import pypeln as pl
 
 def process_image(image_path):
     image = load_image(image_path)
     image = transform_image(image)
     save_image(image_path, image)
 
 files_paths = get_file_paths()
 stage = pl.sync.each(process_image, file_paths, workers=4)
 pl.process.run(stage)
 
```




## filter()
組み込み関数の `filter()` のように振る舞いますが、並行処理が追加されています。


```
 pypeln.process.filter(f: pypeln.process.api.filter.FilterFn, stage: Union[pypeln.process.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, workers: int = 1, maxsize: int = 0, timeout: float = 0, on_start: Callable = None, on_done: Callable = None) -> Union[pypeln.process.stage.Stage[~B], pypeln.utils.Partial[pypeln.process.stage.Stage[~B]]]
```


```
 pypeln.thread.filter(f: pypeln.thread.api.filter.FilterFn, stage: Union[pypeln.thread.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, workers: int = 1, maxsize: int = 0, timeout: float = 0, on_start: Callable = None, on_done: Callable = None) -> Union[pypeln.thread.stage.Stage[~B], pypeln.utils.Partial[pypeln.thread.stage.Stage[~B]]]
```


```
 pypeln.task.filter(f: pypeln.task.api.filter.FilterFn, stage: Union[pypeln.task.stage.Stage[~A], Iterable[~A], AsyncIterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, workers: int = 1, maxsize: int = 0, timeout: float = 0, on_start: Callable = None, on_done: Callable = None) -> Union[pypeln.task.stage.Stage[~A], pypeln.utils.Partial[pypeln.task.stage.Stage[~A]]]
```


```
 pypeln.sync.filter(f: pypeln.sync.api.filter.FilterFn, stage: Union[pypeln.sync.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, workers: int = 1, maxsize: int = 0, timeout: float = 0, on_start: Callable = None, on_done: Callable = None) -> Union[pypeln.sync.stage.Stage[~B], pypeln.utils.Partial[pypeln.sync.stage.Stage[~B]]]
```

- 引数
  -  `f` ー  `f(x) -> bool` のシグニチャを持つ関数
  -  `stage` ー ステージもしくはイテラブル
  -  `workers` ー　ステージで保持するワーカーの数。syncモジュールではAPI互換のために受け入れますが、無視されます。
  -  `maxsize` 　ー　ステージが同時に保持できるオブジェクトの最大数です。 `0` (デフォルト) に設定すると、ステージは無制限に成長することができます。syncモジュールではAPI互換のために受け入れますが、無視されます。
  -  `timeout` 　ー 現在のタスクがまだ完了していない場合、ワーカーを停止させるまでの秒数。デフォルトは  `0` で、これは無制限を意味します。
  -  `on_start` ー  `on_start(worker_info) -> kwargs` のシグニチャを持つ関数を与えます。 `kwargs` には、 `f` と `on_done` に与えるキーワード引数  `dict` を指定することができます。
  -  `on_done` ー　 `on_done(stage_status)` のシグニチャをもつ関数を与えます。この関数は、ワーカーが終了したときに、ワーカーごとに一度だけ実行されます。
- 戻り値
  - 引数 `stage` が指定された場合は  `Stage` を、それ以外の場合は  `Partial` を返します。



 c12_process_filter.py
```
 import time
 from random import random
 
 def slow_gt3(x):
     time.sleep(random()) # 遅い処理を想定...
     return x > 3
 
 def main():
     data = range(10)   # [0, 1, 2, ..., 9]
     stage = pl.process.filter(slow_gt3, data, workers=3, maxsize=4)
 
     data = list(stage) # e.g. [5, 6, 3, 4, 7, 8, 9]
     print(data)
 
 if __name__ == '__main__':
     main()
```


 bash
```
 $ python c12_process_filter.py
 [4, 7, 5, 9, 8, 6]
 
```



```
 In [2]: # %load c22_thread_filter.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_gt3(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:     return x > 3
    ...:
    ...: def main():
    ...:     data = range(10)   # [0, 1, 2, ..., 9]
    ...:     stage = pl.thread.filter(slow_gt3, data, workers=3, maxsize=4)
    ...:
    ...:     data = list(stage) # e.g. [5, 6, 3, 4, 7, 8, 9]
    ...:     print(data)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [5, 4, 8, 9, 6, 7]
 
 In [3]:
 
```



```
 In [2]: # %load c32_task_filter.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_gt3(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:     return x > 3
    ...:
    ...: def main():
    ...:     data = range(10)   # [0, 1, 2, ..., 9]
    ...:     stage = pl.task.filter(slow_gt3, data, workers=3, maxsize=4)
    ...:
    ...:     data = list(stage) # e.g. [5, 6, 3, 4, 7, 8, 9]
    ...:     print(data)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [8, 4, 5, 6, 7, 9]
 
 In [3]:
 
```



```
 In [2]: # %load c42_sync_filter.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_gt3(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:     return x > 3
    ...:
    ...: def main():
    ...:     data = range(10)   # [0, 1, 2, ..., 9]
    ...:     stage = pl.sync.filter(slow_gt3, data, workers=3, maxsize=4)
    ...:
    ...:     data = list(stage) # e.g. [4, 5, 6, 7, 8, 9]
    ...:     print(data)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [4, 5, 6, 7, 8, 9]
 
 In [3]:
 
```




## flat_map()
引数 `f` (あるいは第1引数）に与えた関数をデータ上にマッピングするステージを作成します。ただし、 `pypeln.process.map` とは異なり、イテレータを返します。その名前が示すように、 `flat_map` はこれらのイテレータを平らにして、結果のステージがそれらの要素だけを含むようにします。


```
 pypeln.process.flat_map(f: pypeln.process.api.flat_map.FlatMapFn, stage: Union[pypeln.process.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, workers: int = 1, maxsize: int = 0, timeout: float = 0, on_start: Callable = None, on_done: Callable = None) -> Union[pypeln.process.stage.Stage[~B], pypeln.utils.Partial[pypeln.process.stage.Stage[~B]]]
 
```


```
 pypeln.thread.flat_map(f: pypeln.thread.api.flat_map.FlatMapFn, stage: Union[pypeln.thread.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, workers: int = 1, maxsize: int = 0, timeout: float = 0, on_start: Callable = None, on_done: Callable = None) -> Union[pypeln.thread.stage.Stage[~B], pypeln.utils.Partial[pypeln.thread.stage.Stage[~B]]]
 
```


```
 pypeln.task.flat_map(f: pypeln.task.api.flat_map.FlatMapFn, stage: Union[pypeln.task.stage.Stage[~A], Iterable[~A], AsyncIterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, workers: int = 1, maxsize: int = 0, timeout: float = 0, on_start: Callable = None, on_done: Callable = None) -> Union[pypeln.task.stage.Stage[~B], pypeln.utils.Partial[pypeln.task.stage.Stage[~B]]]
 
```



```
 pypeln.sync.flat_map(f: pypeln.sync.api.flat_map.FlatMapFn, stage: Union[pypeln.sync.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, workers: int = 1, maxsize: int = 0, timeout: float = 0, on_start: Callable = None, on_done: Callable = None) -> Union[pypeln.sync.stage.Stage[~B], pypeln.utils.Partial[pypeln.sync.stage.Stage[~B]]]
 
```

- 引数
  -  `f` ー  `f(x) -> iterable` のシグニチャを持つ関数
  -  `stage` ー ステージもしくはイテラブル
  -  `workers` ー　ステージで保持するワーカーの数。syncモジュールではAPI互換のために受け入れますが、無視されます。
  -  `maxsize` 　ー　ステージが同時に保持できるオブジェクトの最大数です。 `0` (デフォルト) に設定すると、ステージは無制限に成長することができます。syncモジュールではAPI互換のために受け入れますが、無視されます。
  -  `timeout` 　ー 現在のタスクがまだ完了していない場合、ワーカーを停止させるまでの秒数。デフォルトは  `0` で、これは無制限を意味します。
  -  `on_start` ー  `on_start(worker_info) -> kwargs` のシグニチャを持つ関数を与えます。 `kwargs` には、 `f` と `on_done` に与えるキーワード引数  `dict` を指定することができます。
  -  `on_done` ー　 `on_done(stage_status)` のシグニチャをもつ関数を与えます。この関数は、ワーカーが終了したときに、ワーカーごとに一度だけ実行されます。
- 戻り値
  - 引数 `stage` が指定された場合は  `Stage` を、それ以外の場合は  `Partial` を返します。



 c13_process_flat_map.py
```
 import pypeln as pl
 import time
 from random import random
 
 def slow_integer_pair(x):
     time.sleep(random()) # 遅い処理を想定...
 
     if x == 0:
         yield x
     else:
         yield x
         yield -x
 
 def main():
     data = range(10) # [0, 1, 2, ..., 9]
     stage = pl.process.flat_map(
                    slow_integer_pair, data, workers=3, maxsize=4)
 
     v = list(stage) # e.g. [2, -2, 3, -3, 0, 1, -1, 6, -6, 4, -4, ...]
     print(v)
 
 if __name__ == '__main__':
     main()
     
```

 bash
```
 $ python c13_process_flat_map.py
 [1, -1, 0, 3, -3, 4, -4, 2, -2, 5, -5, 6, -6, 7, -7, 8, -8, 9, -9]
 
```



```
 In [2]: # %load c23_thread_flat_map.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_integer_pair(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:
    ...:     if x == 0:
    ...:         yield x
    ...:     else:
    ...:         yield x
    ...:         yield -x
    ...:
    ...: def main():
    ...:     data = range(10) # [0, 1, 2, ..., 9]
    ...:     stage = pl.thread.flat_map(
    ...:                    slow_integer_pair, data, workers=3, maxsize=4)
    ...:
    ...:     v = list(stage) # e.g. [2, -2, 3, -3, 0, 1, -1, 6, -6, 4, -4, ...]
    ...:     print(v)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6, 9, -9, 7, -7, 8, -8]
 
 In [3]:
 
```



```
 In [2]: # %load c33_task_flat_map.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_integer_pair(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:
    ...:     if x == 0:
    ...:         yield x
    ...:     else:
    ...:         yield x
    ...:         yield -x
    ...:
    ...: def main():
    ...:     data = range(10) # [0, 1, 2, ..., 9]
    ...:     stage = pl.task.flat_map(
    ...:                    slow_integer_pair, data, workers=3, maxsize=4)
    ...:
    ...:     v = list(stage) # e.g. [2, -2, 3, -3, 0, 1, -1, 6, -6, 4, -4, ...]
    ...:     print(v)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6, 7, -7, 8, -8, 9, -9]
 
 In [3]:
 
```



```
 In [2]: # %load c43_sync_flat_map.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_integer_pair(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:
    ...:     if x == 0:
    ...:         yield x
    ...:     else:
    ...:         yield x
    ...:         yield -x
    ...:
    ...: def main():
    ...:     data = range(10) # [0, 1, 2, ..., 9]
    ...:     stage = pl.sync.flat_map(
    ...:                    slow_integer_pair, data, workers=3, maxsize=4)
    ...:
    ...:     v = list(stage) # e.g. [0, 1, -1, 2, -2, 3, -3, 4, -4, ...]
    ...:     print(v)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6, 7, -7, 8, -8, 9, -9]
 
 In [3]:
 
```


 `flat_map()` はより一般的な操作で、例えば  `pl.process.map` や  `pl.process.filter` を実装することができます。

 c14_process_flat_map_others.py
```
 import pypeln as pl
 
 pl.process.map(f, stage) = pl.process.flat_map(lambda x: [f(x)], stage)
 pl.process.filter(f, stage) = pl.process.flat_map(
                                    lambda x: [x] if f(x) else [], stage)
```

## from_iterable()
イテラブルからステージを作成します。  `use_thread=True` を与えるとプロセスではなくスレッドを使用します。


```
 pypeln.process.from_iterable(iterable: Union[Iterable[~T], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, use_thread: bool = True, maxsize: int = 0) -> Union[pypeln.process.stage.Stage[~T], pypeln.utils.Partial[pypeln.process.stage.Stage[~T]]]
 
```


```
 pypeln.thread.from_iterable(iterable: Union[Iterable[~T], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, use_thread: bool = True, maxsize: int = 0) -> Union[pypeln.thread.stage.Stage[~T], pypeln.utils.Partial[pypeln.thread.stage.Stage[~T]]]
 
```


```
 pepyln.task.from_iterable(iterable: Union[Iterable[~T], AsyncIterable[~T], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, use_thread: bool = True, maxsize: int = 0) -> Union[pypeln.task.stage.Stage[~T], pypeln.utils.Partial[pypeln.task.stage.Stage[~T]]]
 
```


```
 pypln.sync.from_iterable(iterable: Union[Iterable[~T], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, use_thread: bool = True, maxsize: int = 0) -> Union[pypeln.sync.stage.Stage[~T], pypeln.utils.Partial[pypeln.sync.stage.Stage[~T]]]
 
```

- 引数
  -  `iterable` ー　ソースイテラブル
  -  `use_thread` ー　 `True` (デフォルト) に設定すると、プロセスではなくスレッドを使用してイテラブルを取り込むようになります。スレッドはイテラブルをシリアライズしないため起動が速くなります。イテラブルが遅い計算を行う場合はプロセスの使用を検討してください。process以外のモジュールではAPI互換のために受け入れますが、無視されます。
- 戻り値
  -  `iterable` 引数が指定された場合は  `Stage` を、それ以外の場合は  `Partial` を返します。



 c15_process_from_iterable.py
```
 import pypeln as pl
 import time
 from random import random
 
 def slow_gt3(x):
     time.sleep(random()) # 遅い処理を想定...
     return x > 3
 
 def main():
     data = range(10)   # [0, 1, 2, ..., 9]
     stage = pl.process.from_iterable(data, use_thread=False)
     stage = pl.process.filter(slow_gt3, stage, workers=3, maxsize=4)
 
     data = list(stage) # e.g. [5, 6, 3, 4, 7, 8, 9]
     print(data)
 
 if __name__ == '__main__':
     main()
     
```

 bash
```
  $ python c15_process_from_iterable.py
 [5, 4, 7, 6, 8, 9]
 
```



```
 n [2]: # %load c24_thread_from_iterable.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_gt3(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:     return x > 3
    ...:
    ...: def main():
    ...:     data = range(10)   # [0, 1, 2, ..., 9]
    ...:     stage = pl.thread.from_iterable(data)
    ...:     stage = pl.thread.filter(slow_gt3, stage, workers=3, maxsize=4)
    ...:
    ...:     data = list(stage) # e.g. [5, 6, 3, 4, 7, 8, 9]
    ...:     print(data)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [4, 6, 5, 8, 7, 9]
 
 In [3]:
 
```



```
 In [2]: # %load c34_task_from_iterable.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_gt3(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:     return x > 3
    ...:
    ...: def main():
    ...:     data = range(10)   # [0, 1, 2, ..., 9]
    ...:     stage = pl.task.from_iterable(data)
    ...:     stage = pl.task.filter(slow_gt3, stage, workers=3, maxsize=4)
    ...:
    ...:     data = list(stage) # e.g. [5, 6, 3, 4, 7, 8, 9]
    ...:     print(data)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [4, 5, 6, 7, 8, 9]
 
 In [3]:
 
```


```
 In [2]: # %load c44_sync_from_iterable.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_gt3(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:     return x > 3
    ...:
    ...: def main():
    ...:     data = range(10)   # [0, 1, 2, ..., 9]
    ...:     stage = pl.sync.from_iterable(data)
    ...:     stage = pl.sync.filter(slow_gt3, stage, workers=3, maxsize=4)
    ...:
    ...:     data = list(stage) # e.g. [4, 5, 6, 7, 8, 9]
    ...:     print(data)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [4, 5, 6, 7, 8, 9]
 
 In [3]:
 
```


## map()
データ上に関数fをマッピングするステージを作成します。組み込み関数  `map()` のように振る舞うことを意図していますが、並行処理が追加されています。


```
 pypeln.process.map(f: pypeln.process.api.map.MapFn, stage: Union[pypeln.process.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, workers: int = 1, maxsize: int = 0, timeout: float = 0, on_start: Callable = None, on_done: Callable = None) -> Union[pypeln.process.stage.Stage[~B], pypeln.utils.Partial[pypeln.process.stage.Stage[~B]]]
 
```


```
 pypeln.thread.map(f: pypeln.thread.api.map.MapFn, stage: Union[pypeln.thread.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, workers: int = 1, maxsize: int = 0, timeout: float = 0, on_start: Callable = None, on_done: Callable = None) -> Union[pypeln.thread.stage.Stage[~B], pypeln.utils.Partial[pypeln.thread.stage.Stage[~B]]]
 
```


```
 pypeln.task.map(f: pypeln.task.api.map.MapFn, stage: Union[pypeln.task.stage.Stage[~A], Iterable[~A], AsyncIterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, workers: int = 1, maxsize: int = 0, timeout: float = 0, on_start: Callable = None, on_done: Callable = None) -> Union[pypeln.task.stage.Stage[~B], pypeln.utils.Partial[pypeln.task.stage.Stage[~B]]]
 
```


```
 pypeln.sync.map(f: pypeln.sync.api.map.MapFn, stage: Union[pypeln.sync.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, workers: int = 1, maxsize: int = 0, timeout: float = 0, on_start: Callable = None, on_done: Callable = None) -> Union[pypeln.sync.stage.Stage[~B], pypeln.utils.Partial[pypeln.sync.stage.Stage[~B]]]
 
```

- 引数
  -  `f` ー  `f(x) -> y` のシグニチャを持つ関数
  -  `stage` ー ステージもしくはイテラブル
  -  `workers` ー　ステージで保持するワーカーの数。syncモジュールではAPI互換のために受け入れますが、無視されます。
  -  `maxsize` 　ー　ステージが同時に保持できるオブジェクトの最大数です。 `0` (デフォルト) に設定すると、ステージは無制限に成長することができます。syncモジュールではAPI互換のために受け入れますが、無視されます。
  -  `timeout` 　ー 現在のタスクがまだ完了していない場合、ワーカーを停止させるまでの秒数。デフォルトは  `0` で、これは無制限を意味します。
  -  `on_start` ー  `on_start(worker_info) -> kwargs` のシグニチャを持つ関数を与えます。 `kwargs` には、 `f` と `on_done` に与えるキーワード引数  `dict` を指定することができます。
  -  `on_done` ー　 `on_done(stage_status)` のシグニチャをもつ関数を与えます。この関数は、ワーカーが終了したときに、ワーカーごとに一度だけ実行されます。
- 戻り値
  - 引数 `stage` が指定された場合は  `Stage` を、それ以外の場合は  `Partial` を返します。

 c16_process_map.py
```
 import pypeln as pl
 import time
 from random import random
 
 def slow_add1(x):
     time.sleep(random()) # <= some slow computation
     return x + 1
 
 def main():
     data = range(10) # [0, 1, 2, ..., 9]
     stage = pl.process.map(slow_add1, data, workers=3, maxsize=4)
 
     data = list(stage) # e.g. [2, 1, 5, 6, 3, 4, 7, 8, 9, 10]
     print(data)
 
 if __name__ == '__main__':
     main()
 
```


 bash
```
 $ python c16_process_map.py
 [1, 2, 4, 5, 6, 7, 3, 8, 9, 10]
 
```



```
 In [2]: # %load c25_thread_map.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_add1(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:     return x + 1
    ...:
    ...: def main():
    ...:     data = range(10) # [0, 1, 2, ..., 9]
    ...:     stage = pl.thread.map(slow_add1, data, workers=3, maxsize=4)
    ...:
    ...:     data = list(stage) # e.g. [2, 1, 5, 6, 3, 4, 7, 8, 9, 10]
    ...:     print(data)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [3, 2, 1, 6, 4, 5, 9, 8, 7, 10]
 
 In [3]:
 
```



```
 In [2]: # %load c35_task_map.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_add1(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:     return x + 1
    ...:
    ...: def main():
    ...:     data = range(10) # [0, 1, 2, ..., 9]
    ...:     stage = pl.task.map(slow_add1, data, workers=3, maxsize=4)
    ...:
    ...:     data = list(stage) # e.g. [2, 1, 5, 6, 3, 4, 7, 8, 9, 10]
    ...:     print(data)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
 
 In [3]:
 
```



```
 In [2]: # %load c45_sync_map.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_add1(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:     return x + 1
    ...:
    ...: def main():
    ...:     data = range(10) # [0, 1, 2, ..., 9]
    ...:     stage = pl.sync.map(slow_add1, data, workers=3, maxsize=4)
    ...:
    ...:     data = list(stage) # e.g. [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ...:     print(data)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
 
 In [3]:
 
```


## ordered()
パイプラインのソースイテラブル(複数可) で作成された順序に基づいて要素をソートするステージを作成します。


```
 pypeln.process.ordered(stage: Union[pypeln.process.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, maxsize: int = 0) -> Union[pypeln.process.stage.Stage[~A], pypeln.utils.Partial[pypeln.process.stage.Stage[~A]]]
 
```


```
 pypln.thread.ordered(stage: Union[pypeln.thread.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, maxsize: int = 0) -> Union[pypeln.thread.stage.Stage[~A], pypeln.utils.Partial[pypeln.thread.stage.Stage[~A]]]
 
```


```
 pypln.task...ordered(stage: Union[pypeln.task.stage.Stage[~A], Iterable[~A], AsyncIterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, maxsize: int = 0) -> Union[pypeln.task.stage.Stage[~A], pypeln.utils.Partial[pypeln.task.stage.Stage[~A]]]
 
```


```
 pypeln.sync.ordered(stage: Union[pypeln.sync.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, maxsize: int = 0) -> Union[pypeln.sync.stage.Stage[~A], pypeln.utils.Partial[pypeln.sync.stage.Stage[~A]]]
 
```

- 引数
  -  `stages` ー　ステージのリスト、もしくはイテラブル
  -  `maxsize` ー ステージが同時に保持できるオブジェクトの最大数です。 `0` (デフォルト) に設定すると、ステージは無制限に成長することができます。
- 戻り値
  - もし  `stage` 引数が与えられると、この関数はイテラブルを返し、そうでなければ  `Partial` を返します。



 c17_process_ordered.py
```
 import pypeln as pl
 import random
 import time
 
 def slow_squared(x):
     time.sleep(random.random())
 
     return x ** 2
 
 def main():
     stage = range(5)
     stage = pl.process.map(slow_squared, stage, workers = 2)
     stage = pl.process.ordered(stage)
 
     print(list(stage)) # [0, 1, 4, 9, 16]
 
 if __name__ == '__main__':
     main()
     
```


 bash
```

 [0, 1, 4, 9, 16]
 
```



```
 In [2]: # %load c26_thread_ordered.py
    ...: import pypeln as pl
    ...: import random
    ...: import time
    ...:
    ...: def slow_squared(x):
    ...:     time.sleep(random.random())
    ...:
    ...:     return x ** 2
    ...:
    ...: def main():
    ...:     stage = range(5)
    ...:     stage = pl.thread.map(slow_squared, stage, workers = 2)
    ...:     stage = pl.thread.ordered(stage)
    ...:
    ...:     print(list(stage)) # [0, 1, 4, 9, 16]
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [0, 1, 4, 9, 16]
 
 In [3]:
 
```



```
 In [2]: # %load c36_task_ordered.py
    ...: import pypeln as pl
    ...: import random
    ...: import time
    ...:
    ...: def slow_squared(x):
    ...:     time.sleep(random.random())
    ...:
    ...:     return x ** 2
    ...:
    ...: def main():
    ...:     stage = range(5)
    ...:     stage = pl.task.map(slow_squared, stage, workers = 2)
    ...:     stage = pl.task.ordered(stage)
    ...:
    ...:     print(list(stage)) # [0, 1, 4, 9, 16]
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [0, 1, 4, 9, 16]
 
 In [3]:
 
```



```
 In [2]: # %load c46_sync_ordered.py
    ...: import pypeln as pl
    ...: import random
    ...: import time
    ...:
    ...: def slow_squared(x):
    ...:     time.sleep(random.random())
    ...:
    ...:     return x ** 2
    ...:
    ...: def main():
    ...:     stage = range(5)
    ...:     stage = pl.sync.map(slow_squared, stage, workers = 2)
    ...:     stage = pl.sync.ordered(stage)
    ...:
    ...:     print(list(stage)) # [0, 1, 4, 9, 16]
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [0, 1, 4, 9, 16]
 
 In [3]:
 
```



## run()
1つまたは複数のステージを、そのイテレータが要素を使い果たすまで繰り返し処理します。


```
 pypln.process.run(*stages: Union[pypeln.process.stage.Stage[~A], Iterable[~A]], maxsize: int = 0) -> None
 
```


```
 pypln.thread.run(*stages: Union[pypeln.thread.stage.Stage[~A], Iterable[~A]], maxsize: int = 0) -> None
 
```


```
 pypeln.task.run(*stages: Union[pypeln.task.stage.Stage[~A], Iterable[~A], AsyncIterable[~A]], maxsize: int = 0) -> None
 
```


```
 pypeln.sync.run(*stages: Union[pypeln.sync.stage.Stage[~A], Iterable[~A]], maxsize: int = 0) -> None
 
```


- 引数
  -  `stages` ー　ステージのリスト、もしくはイテラブル
  -  `maxsize` ー ステージが同時に保持できるオブジェクトの最大数です。 `0` (デフォルト) に設定すると、ステージは無制限に成長することができます。syncモジュールではAPI互換のために受け入れますが、無視されます。
- 戻り値
  -  `None` 


 c18_process_run.py
```
 import pypeln as pl
 import time
 from random import random
 
 def get_data():
     return [1, 2, 3, 4, 5, 6, 7]
 
 def slow_add(x):
     time.sleep(random()) # 遅い処理を想定...
     print(x+1)
     return x + 1
 
 def main():
     data = get_data()
     stage = pl.process.each(slow_add, data, workers=3)
     pl.process.run(stage)
 
 if __name__ == '__main__':
     main()
     
```

 bash
```
 $ python c18_process_run.py
 4
 2
 3
 5
 6
 8
 7
 
```



```
 In [2]: # %load c27_thread_run.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def get_data():
    ...:     return [1, 2, 3, 4, 5, 6, 7]
    ...:
    ...: def slow_add(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:     print(x+1)
    ...:     return x + 1
    ...:
    ...: def main():
    ...:     data = get_data()
    ...:     stage = pl.thread.each(slow_add, data, workers=3)
    ...:     pl.process.run(stage)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 2
 4
 6
 3
 5
 7
 8
 
 In [3]:
 
```



```
 In [2]: # %load c37_task_run.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def get_data():
    ...:     return [1, 2, 3, 4, 5, 6, 7]
    ...:
    ...: def slow_add(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:     print(x+1)
    ...:     return x + 1
    ...:
    ...: def main():
    ...:     data = get_data()
    ...:     stage = pl.task.each(slow_add, data, workers=3)
    ...:     pl.process.run(stage)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 2
 3
 4
 5
 6
 7
 8
 
 In [3]:
 
```



```
 In [2]: # %load c47_sync_run.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def get_data():
    ...:     return [1, 2, 3, 4, 5, 6, 7]
    ...:
    ...: def slow_add(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:     print(x+1)
    ...:     return x + 1
    ...:
    ...: def main():
    ...:     data = get_data()
    ...:     stage = pl.sync.each(slow_add, data, workers=3)
    ...:     pl.process.run(stage)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 2
 3
 4
 5
 6
 7
 8
 
 In [3]:
```



## to_iterable()
ステージからイテラブルを作成します。この関数は、出力ステージがどのように使用されるかをより細かく制御したい場合に使用します。特に、引数  `maxsize` を設定することで、イテラブルの取り出しが遅い場合に OOM エラーを回避するのに役立ちます。（Linuxのカーネルがメモリが不足するときにメモリを使用するプロセスを無慈悲に強制終了する仕組み）


```
 pypeln.process.to_iterable(stage: Union[pypeln.process.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, maxsize: int = 0, return_index: bool = False) -> Union[Iterable[~A], pypeln.utils.Partial[Iterable[~A]]]
 
```


```
 pypeln.thread.to_iterable(stage: Union[pypeln.thread.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, maxsize: int = 0, return_index: bool = False) -> Union[Iterable[~A], pypeln.utils.Partial[Iterable[~A]]]
 
```


```
 pypeln.task.to_iterable(stage: Union[pypeln.task.stage.Stage[~A], Iterable[~A], AsyncIterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, maxsize: int = 0, return_index: bool = False) -> Union[Iterable[~A], pypeln.utils.Partial[Iterable[~A]]]
 
```


```
 pypeln.sync.to_iterable(stage: Union[pypeln.sync.stage.Stage[~A], Iterable[~A], pypeln.utils.Undefined] = <pypeln.utils.Undefined object at 0x116a69240>, maxsize: int = 0, return_index: bool = False) -> Union[Iterable[~A], pypeln.utils.Partial[Iterable[~A]]]
```


- 引数
  -  `stages` ー　ステージのリスト、もしくはイテラブル
  -  `maxsize` ー ステージが同時に保持できるオブジェクトの最大数です。 `0` (デフォルト) に設定すると、ステージは無制限に成長することができます。syncモジュールではAPI互換のために受け入れますが、無視されます。

- 戻り値
  - もし  `stage` 引数が与えられると、この関数はイテラブルを返し、そうでなければ  `Partial` を返します。


 c19_process_to_iterable.py
```
 import pypeln as pl
 import time
 from random import random
 
 def slow_gt3(x):
     time.sleep(random()) # 遅い処理を想定...
     return x > 3
 
 def main():
     data = range(10)   # [0, 1, 2, ..., 9]
     stage = pl.process.filter(slow_gt3, data, workers=3, maxsize=4)
 
     data = pl.process.to_iterable(stage)
     for d in data:
         print(d)
 
 if __name__ == '__main__':
     main()
     
```


 bash
```
 
 $ python c19_process_to_iterable.py
 4
 6
 5
 8
 7
 9
 
```



```
 In [2]: # %load c28_thread_to_iterable.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_gt3(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:     return x > 3
    ...:
    ...: def main():
    ...:     data = range(10)   # [0, 1, 2, ..., 9]
    ...:     stage = pl.thread.filter(slow_gt3, data, workers=3, maxsize=4)
    ...:
    ...:     data = pl.thread.to_iterable(stage)
    ...:     for d in data:
    ...:         print(d)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 5
 6
 4
 8
 7
 9
 
 In [3]:
 
```




```
 In [2]: # %load c38_task_to_iterable.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_gt3(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:     return x > 3
    ...:
    ...: def main():
    ...:     data = range(10)   # [0, 1, 2, ..., 9]
    ...:     stage = pl.task.filter(slow_gt3, data, workers=3, maxsize=4)
    ...:
    ...:     data = pl.task.to_iterable(stage)
    ...:     d = list(data)
    ...:     print(d)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [4, 5, 6, 7, 8, 9]
 
 In [3]:
 
```



```
 In [2]: # %load c48_sync_to_iterable.py
    ...: import pypeln as pl
    ...: import time
    ...: from random import random
    ...:
    ...: def slow_gt3(x):
    ...:     time.sleep(random()) # 遅い処理を想定...
    ...:     return x > 3
    ...:
    ...: def main():
    ...:     data = range(10)   # [0, 1, 2, ..., 9]
    ...:     stage = pl.sync.filter(slow_gt3, data, workers=3, maxsize=4)
    ...:
    ...:     data = pl.sync.to_iterable(stage)
    ...:     d = list(data)
    ...:     print(d)
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 [4, 5, 6, 7, 8, 9]
 
 In [3]:
 
```


### ユーザー定義

 `on_start` が返す辞書内の任意の要素は、引数 `f` と  `on_done` で与える関数の引数として使用されます。




# テストの実行
ソースコードのレポジトリには、コンテナ（DockerまたはPodman）を使って環境構築を行いテストを実行するためのサンプルスクリプトが提供されています。テストを実行してみてください。

 test-version.sh
```
 #!/bin/bash
 # run-test - A script to run tests pypeln in a container
 # can recive an optional declaring python version
 set -e
 
 kPYTHON_VERSIONS='^[3]\.[0-9]{1,2}$'
 kDEFAULT_VERSION=3.8
 
 
 container_runner () {
     if [[ -z "$1" ]]; then
         py_version="$kDEFAULT_VERSION"
     else
         py_version=$1
     fi
 
     if hash podman 2>/dev/null; then
         podman build --build-arg PY_VERSION="$py_version" -t pypeln .
         podman run -it --rm  -v "$(pwd)":/usr/src/app:Z pypeln:latest
     else
         docker build --build-arg PY_VERSION="$py_version" -t pypeln .
         docker run -it --rm  -v "$(pwd)":/usr/src/app:Z pypeln:latest
     fi
 }
 
 if [[ $1 =~ $kPYTHON_VERSIONS ]] || [[ -z "$1" ]]; then
     container_runner "$1"
 else
     echo "Check python version"
 fi
 
```

このスクリプトは、テストをチェックするための Python のバージョンを受け取ることもできます。

 bash
```
 $ bash scripts/test-version.sh 3.7
 
```

## プログレスバーの表示
tqdm モジュールと組み合わせるとパイプラインの進捗状況のプログレスバーを表示させることができます。

  python
```
 In [2]: # %load c50_probress_bar.py
    ...: from aiohttp import ClientSession, TCPConnector
    ...: import asyncio
    ...: import pypeln as pl
    ...: from tqdm.asyncio import trange, tqdm
    ...: import time
    ...:
    ...: limit = 1
    ...: users = list(range(1,10))
    ...:
    ...: async def fetch(users, session):
    ...:     time.sleep(1)
    ...:     pbar.update(1)
    ...:
    ...: with tqdm(total=len(users)) as pbar:
    ...:     pl.task.each(
    ...:         fetch,
    ...:         users,
    ...:         workers=limit,
    ...:         on_start=lambda: dict(session=ClientSession(connector=TCPConnect
    ...: or(limit=None,ssl=False))),
    ...:         on_done=lambda session: session.close(),
    ...:         run=True,
    ...:     )
    ...:
    ...:
 100%|█████████████████████████████████████████████| 9/9 [00:09<00:00,  1.01s/it]
 
 In [3]:
 
```



# 参考

- pypeln
  - [PyPI - pypeln ](https://pypi.org/project/pypeln/)
  - [ソースコード ](https://github.com/cgarciae/pypeln/)
  - [公式ドキュメント ](https://cgarciae.github.io/pypeln/)

#パイプライン処理


