watchpointsモジュールを使ってみよう
=================

## watchpoints について
watchpointsは、Linuxで使用されるデバッガgdbのwatchpointsに似た動作をするモニターツールで、指定したPythonの変数やオブジェクトをモニターすることができます。使いやすく直感的に使えるのが特徴です。

## インストール
watchpoints のインストールは pip コマンドで行います。

 bash
```
 $ pip install watchpoints
```


## 使用方法
watchpoints の使用方法は簡単です。モニターしたいPythonオブジェクトを `watchpoints.watch()` に引数で与えるだけです。
オブジェクトが変更されるたびに、 `watch()` が呼び出される前後でのそのオブジェクトの値を表示します。

 watchpoints_demo1.py
```
 from watchpoints import watch
 
 a = 0
 watch(a)
 a = 1    
```

これを実行すると次のように表示されます。

 bash
```
 $ python watchpoints_demo1.py
 ====== Watchpoints Triggered ======
 Call Stack (most recent call last):
   <module> (/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_sample.py:5):
 >   a = 1
 a:
 0
 ->
 1
 
```

 `watch()` は変数だけでなく、オブジェクトの変更もモニターしています。

 watchpoints_demo2.py
```
 from watchpoints import watch
 
 a = []
 watch(a)
 a.append(1)    # Trigger
 a = {}         # Trigger
 
```

これを実行すると次のようになります。

 bash
```
 % python  watchpoints_demo2.py
 ====== Watchpoints Triggered ======
 Call Stack (most recent call last):
   <module> (/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_demo2.py:5):
 >   a.append(1)    # Trigger
 a:
 []
 ->
 [1]
 
 ====== Watchpoints Triggered ======
 Call Stack (most recent call last):
   <module> (/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_demo2.py:6):
 >   a = {}         # Trigger
 a:
 [1]
 ->
 {}
 
```

それだけでなく、変数の変更後のオブジェクトの変更を追跡することができます。

 watchpoints_demo3.py
```
 from watchpoints import watch
 
 a = []
 watch(a)
 a = {}      # Trigger
 a["a"] = 2  # Trigger
```

 bash
```
 
  % python watchpoints_demo3.py
 ====== Watchpoints Triggered ======
 Call Stack (most recent call last):
   <module> (/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_demo3.py:5):
 >   a = {}      # Trigger
 a:
 []
 ->
 {}
 
 ====== Watchpoints Triggered ======
 Call Stack (most recent call last):
   <module> (/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_demo3.py:6):
 >   a["a"] = 2  # Trigger
 a:
 {}
 ->
 {'a': 2}
 
```

同じスコープでなくても、オブジェクトが変更されるたびに動作します。

 watchpoints_demo4.py
```
 from watchpoints import watch
 
 def func(var):
     var["a"] = 1
 
 a = {}
 watch(a)
 func(a)
 
```


 bash
```
 % python  watchpoints_demo4.py
 ====== Watchpoints Triggered ======
 Call Stack (most recent call last):
   <module> (/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_demo4.py:8):
 >   func(a)
   func (/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_demo4.py:4):
 >   var["a"] = 1
 a:
 {}
 ->
 {'a': 1}
 
```

 `watch()` に複数の引数を与えることができ、オブジェクトの属性や、リストや辞書の特定の要素を監視することもできます。

 watchpoints_demo5.ppy
```
 from watchpoints import watch
 
 class MyObj:
     def __init__(self):
         self.a = 0
 
 obj = MyObj()
 d = {"a": 0}
 watch(obj.a, d["a"])  # こんなこともできる
 obj.a = 1             # Trigger
 d["a"] = 1            # Trigger
```

 bash
```
 % python  watchpoints_demo5.py
 ====== Watchpoints Triggered ======
 Call Stack (most recent call last):
   <module> (/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_demo5.py:10):
 >   obj.a = 1             # Trigger
 obj.a:
 0
 ->
 1
 
 ====== Watchpoints Triggered ======
 Call Stack (most recent call last):
   <module> (/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_demo5.py:11):
 >   d["a"] = 1            # Trigger
 d["a"]:
 0
 ->
 1
 
```

これにより、興味のある特定のオブジェクトを絞り込むことができるかもしれません。

## 変数とオブジェクト
オブジェクトに対して  `watch()` を実行すると、実際にはオブジェクトとそれを保持する変数の両方を追跡することになります。ほとんどの場合、それで何もっ問題ありませんが、どちらを追跡したいかを正確に設定することもできます。

 watchpoints_obj_val.py
```
 from watchpoints import watch
 
 a = []
 watch(a, track="object")
 a.append(1)   # Trigger
 a = {}        # オブジェクトが変わっていないので、何も起きない
 
 a = []
 watch(a, track="variable")
 a.append(1)   #  'a' は同じオブジェクトなので、何も起きない
 a = {}        # Trigger
 
```

 bash
```
 % python  watchpoints_obj_val.py
 ====== Watchpoints Triggered ======
 Call Stack (most recent call last):
   <module> (/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_obj_val.py:5):
 >   a.append(1)   # Trigger
 a:
 []
 ->
 [1]
 
 ====== Watchpoints Triggered ======
 Call Stack (most recent call last):
   <module> (/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_obj_val.py:11):
 >   a = {}        # Trigger
 a:
 []
 ->
 {}
 
```


## 条件付きの監視
条件付きの監視を行うために、 `when` 引数に追加の条件フィルタとして関数を与えることができます。関数  `func(obj)` を渡すと、 `watch()` が発動したタイミングでコールバック関数を呼び出します。コールバック関数が `True` を返したときにオブジェクトの値が表示されます。

 watchpoints_when.py
```
 from watchpoints import watch
 
 a = 0
 watch(a, when=lambda x: x > 0)
 a = -1    # nothing will happen
 a = 1     # Triggertchpoints_when.py
 
```

## オブジェクト比較とディープコピー
通常、ネストされたオブジェクトの比較は面倒なものです。複雑にカスタマイズされたオブジェクトを比較するための、標準的な方法を見つけるのは難しいです。デフォルトでは、watchpoints はオブジェクトの浅いコピー(shallow copy)を行います。 `watch()` に `deepcopy=True` を渡すことで、この動作をオーバーライドすることができます。


```
 watch(a, deepcopy=True)
```

watchpoints は、ユーザー定義クラスの `__eq__()` メソッドを最初に呼び出そうとします。 `__eq__()` が実装されていない場合、watchpoints はshallow copyを使用している場合はオブジェクトの  `__dict__` （基本的には属性値）を比較し、deepcopyを使用している場合は `NotImplementedError` を発生させます。

この理由は、複雑な構造をディープコピーした場合、ユーザー定義の `__eq__()` メソッドがなければ、watchpoints が同じオブジェクトであるかどうかを判断する方法がないからです。

## コピーと比較のカスタマイズ
独自のデータ構造に対して、カスタマイズされたコピー関数を `copy` 引数で、カスタマイズされた比較関数を `cmp` 引数で `watch()` に与えることができます。

watchpointsは、与えられた `copy` 関数を使って参照用のオブジェクトをコピーし、与えられた `cmp` 関数を使ってそのオブジェクトが変更されたかどうかをチェックします。 `copy` 関数や `cmp` 関数が提供されない場合は、前述のようにデフォルトの動作となります。

 `cmp` 引数に与える関数は，2つのオブジェクトを引数として取り，それらのオブジェクトが異なるかどうかを表すブール値を返す必要があります。


```
 def my_cmp(obj1, obj2):
     return obj1.id != obj2.id
 
 watch(a, cmp=my_cmp)
```

 `copy` 引数に与える関数は、オブジェクトを受け取り、そのコピーを返す必要があります。


```
 def my_copy(obj):
     return MyObj(id=obj.id)
 
 watch(a, copy=my_copy)
```

## スタック制限
 `watch.config()` で出力されるコール・スタックに制限を指定することができます。デフォルトの値は 5 で、正の整数なら何でもOKです。 `None` を指定すると、無制限のコールスタックとなり、すべてのフレームが出力されます。


```
 watch.config(stack_limit=10)
 
```

また、watchの引数にstack_limitを渡すことで、監視対象の変数ごとに異なるスタックリミットを設定することができます。


```
 watch(a, stack_limit=10)
 
```



## コールバックのカスタマイズ
独自のフォーマットで出力したい場合や、出力以上のことをしたい場合もあるかもしれません。監視変数に独自のコールバックを使用することができます。


```
 watch(a, callback=my_callback)
```

コールバック関数は3つの引数を取ります。


```
 def my_callback(frame, elem, exec_info)
     pass
```
	

-  `frame` ：変化が検出されたときの現在のフレームです。
-  `elem` ：WatchElement オブジェクトです。
-  `exec_info` ：変数を変更した行の  `(funcname, filename, lineno)` のタプルです。

グローバルに設定したい場合は、 `watch.config()` で設定します。


```
 watch.config(callback=my_callback)
 
```

デフォルトに戻したい場合は、 `restore()` を呼び出します。


```
 watch.restore()
```


## 異なるストリームへの出力
 `print()` 関数とおなじように、 `watch()` の出力ストリームを `file` 引数で選択することができます。デフォルトでは、 `sys.stderr` です。

 watchpoints_file.py
```
 from watchpoints import watch
 
 with open("watch.log", "w") as f:
     a = 0
     watch(a, file=f)
     a = 1
```

オブジェクトが変更されたときに、ストリームが利用可能である必要があることに注意してください。そのため、以下のコードでは動作しません。

 watchpoints_file_bad.py
```
 from watchpoints import watch
 
 a = 0
 with open("watch.log", "w") as f:
     watch(a, file=f)
 a = 1
```

 `watch()` の引数  `file` にファイル名を与えることもできます。


```
 watch(obj, filel='watch.log')
```

グローバルに設定する場合は、  `watch.config()` で設定します。


```
 watch.config(file='watch.log')
```

独自の出力
デフォルトのobjprintではなく，独自のプリンタ関数を使ってオブジェクトを印刷したいときは、 `custom_printer` 引数を使用します。

 watchpoints_custom_print.py
```
 from watchpoints import watch
 from pprint import pprint
 
 a = 0
 watch(a, custom_printer=pprint)
 a = 1
```

これも `watch.config()` でグローバルに設定することができます。

```
 from pprint import pprint
 watch.config(custom_printer=pprint)
 
```


## pdbとの連携

デバッグ工程で変数をモニターするとき、その変数に対してなにか操作をしたいときがあります。そうしたときは、
 `watch.config(pdb=True) ` と設定しておきます。すろと、 `watch()` に与えたオブジェクトが変更されときに  `pdb.set_trace()` が呼び出すようになります。
pdbを起動しているときに、 `quit` や  `Ctrl-D` でpdbを終了すると、次のオブジェクトの変更で再びpdbが起動します。 `continue` であれば、そのままコードは継続されます。



```
 from watchpoints import watch
 
 def square(n):
     result = n ** 2
     print(result)
     return result
 
 def main():
     for i in range(1,10):
         watch(i)
         square(i)
 
 if __name__ == "__main__":
     watch.config(pdb=True) 
     main()
     
```

 bash
```
 % python watchpoints_pdb.py
 1
 ====== Watchpoints Triggered ======
 Call Stack (most recent call last):
   <module> (/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_pdb.py:15):
 >   main()
   main (/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_pdb.py:9):
 >   for i in range(1,10):
 i:
 1
 ->
 2
 
 [1] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_pdb.py(10)main()
 -> watch(i)
 (Pdb++)
```


## 組み込み関数に登録
通常であれば、 `watch()` を呼び出すすべてのファイルで watchpoints をインポートする必要があります。しかし、これは地味に面倒なことになります。 watchpoints では `__main__` のどこかで `watch.install()` を呼び出しておくと、以後は組み込み関数として  `watch()` を利用することができます。


```
 def square(n):
     result = n ** 2
     print(result)
     return result
 
 def main():
     for i in range(1,10):
         watch(i)
         square(i)
 
 if __name__ == "__main__":
     from watchpoints import watch
     watch.install()
     main()
```

 `watch.install('obj_watch')` のようにすると、関数名を変えることができます。

 watchpoints_install__func.py
```
 def square(n):
     result = n ** 2
     print(result)
     return result
 
 def main():
     for i in range(1,10):
         obj_watch(i)
         square(i)
 
 if __name__ == "__main__":
     from watchpoints import watch
     watch.install('obj_watch')
     main()
    
```

## unwatch()
対象のオブジェクトの監視を終える場合は、  `unwatch()` を呼び出します。

 watchpoints_unwatch.py
```
 from watchpoints import watch, unwatch
 
 a = 0
 watch(a)
 a = 1           # trigger
 unwatch(a)
 a = 2           # nothing will happen
 
```

 bash
```
 % python watchpoints_unwatch.py
 ====== Watchpoints Triggered ======
 Call Stack (most recent call last):
   <module> (/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_unwatch.py:5):
 >   a = 1           # trigger
 a:
 0
 ->
 1
 
```


## エイリアス
監視している変数にエイリアスを与えることで、エリアスを指定して  `unwatch()` できるようになります。また、変数名の代わりにエイリアスが表示されます

 watchpoints_alias.py
```
 rom watchpoints import watch, unwatch
 
 def myfunc():
     a = 0
     watch(a, alias="myfunc")
     a = 1
 
 myfunc()
 
 # 何かしらの処理...
 
 unwatch("myfunc")
 a = 3
 
```

 bash
```
 % python  watchpoints_alias.py
 ====== Watchpoints Triggered ======
 Call Stack (most recent call last):
   <module> (/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_alias.py:8):
 >   myfunc()
   myfunc (/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_alias.py:6):
 >   a = 1
 myfunc:
 0
 ->
 1
 
```


## マルチスレッド対応
IPython で watchpoints を使用すると、Python のときと表示がすこし変わってしまいます。この理由は IPython がスレッドを使用してPython コードを実行していることによります。watchpointsは、マルチスレッドに対応したネイティブ・スレッド・ライブラリをサポートしていて。どのスレッドが値を変更しているかもわかるようになっているからです。

 bash
```
 % ipython watchpoints_unwatch.py
 ====== Watchpoints Triggered ======
 ---- MainThread ----
 Call Stack (most recent call last):
   _run_cmd_line_code (/Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/site-packages/IPython/core/shellapp.py:453):
 >   self._exec_file(fname, shell_futures=True)
   _exec_file (/Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/site-packages/IPython/core/shellapp.py:378):
 >   self.shell.safe_execfile(full_filename,
   safe_execfile (/Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/site-packages/IPython/core/interactiveshell.py:2764):
 >   py3compat.execfile(
   execfile (/Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/site-packages/IPython/utils/py3compat.py:168):
 >   exec(compiler(f.read(), fname, 'exec'), glob, loc)
   <module> (/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Watchpoints/watchpoints_unwatch.py:5):
 >   a = 1           # trigger
 a:
 0
 ->
 1
```


## まとめ
watchpoints を使うと簡単にPythonオブジェクトを監視することができます。ロギングやpdbとも連携できるため、デバッグでの利用価値は高い便利なモジュールです。


## 参考
- [watchpoints ソースコード ](https://github.com/gaogaotiantian/watchpoints)
- Python公式ドキュメント
  - [pdb --- Python デバッガ  ](https://docs.python.org/ja/3/library/pdb.html)


