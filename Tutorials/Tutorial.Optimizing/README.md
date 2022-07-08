Pythonチュートリアル：スクリプトの高速化
=================

![](https://gyazo.com/153a339305d78fc4fa4850753e4b1594.png)

### ベースのPythonを変更してみる
Anaconda Python は Intel Math Kernel Library ([oneMKL ](https://www.xlsoft.com/jp/products/intel/perflib/mkl/index.html)) を使ってリンクされているため、特にIntel系のCPUでは最適化された性能を発揮することができます。
Anaconda Python をベースにしたIntel Distribution for Pyhonが[同包 ](https://www.xlsoft.com/jp/products/intel/python/index.html)されています。
Intel社はこれまで有償ソフトであったコンパイラ他の製品を [oneAPI ](https://www.oneapi.com/) として再編し無料で使えるようにしています。
[oneAPI Base Toolkit ](https://software.intel.com/content/www/us/en/develop/articles/free-intel-software-developer-tools.html) をインストールすると、このIntel Distribuition for Python を使用することができます。次図は、MKLでビルドされたIntel Distribution for Python の numpy （グラフでは青）と、pip でインストールできる numpy（グラフでは赤）の性能比較で、数値が高い（グラフが高い）ほど性能がよいことを表しています。

![](https://gyazo.com/997d0c2145a60494fe6c843b95be9601.png)
出典：https://www.xlsoft.com/jp/products/intel/python/index.html

> Python での実行環境を管理するツールとして conda の他に pyenv などがります。
> 演算性能は、Webアプリケーションではそれほど重要ではありませんが、機械学習や
> 科学技術計算の領域では演算性能は無視できなくなります。
> 上図をみても MKL がリンクされた numpy の性能差は圧倒的です
> 性能重視するのであれば、Anaconda Pythonおよび conda環境をお勧めします。

### numpy と scipy をMKLを使ってビルドしてみる
プロジェクトの方針で Anaconda Python や Intel Distributed Python が使用できない場合があります。
そうした場合には、次の手順で numpy と scipy を MKL を使ってビルドした版を作成して、インストールしてみましょう。

まず、ビルドに必要なコンパイラなどをインストールします。
 bash Ubuntu
```
 $ apt install build-essential
```

 bash RedHat/CentOS
```
 $ yum groupinstall development
```

oneAPI がリリースされたときから、MKLライブラリもpip で簡単にインストールできるようになりました。

 bash
```
 $ pip install mkl mkl-devel mkl-include 
```


pip がどのディレクトリにインストールしたのかを調べます。
 bash
```
 $ pip list --user
 Package      Version
 ------------ --------
 intel-openmp 2021.2.0
 mkl          2021.2.0
 mkl-devel    2021.2.0
 mkl-include  2021.2.0
 tbb          2021.2.0
 
 $ find $HOME/.local | egrep "/libmkl_rt.so|/mkl.h"
 /home/iisaka/.local/include/mkl.h
 /home/iisaka/.local/lib/libmkl_rt.so.1
```

mkl 2021.2 では共有ライブラリがうまく作成されていないため。このままではnumpy と scipy びビルドでMKLを見つけてくれません。
暫定的に次のようにシンボリックリンクを設定しました。

 FIX-mkl.sh
```
 #!/bin/bash 
 cd $HOME/.local/lib
 for F in *.so.[0-9]*
 do
     [ -f ${F%.*} ] || ln -s $F ${F%.*}
 done
```

環境変数 LD_LIBRARY_PATH にMKLがインストールされたディレクトリを設定しておきます。
 bash
```
 $ export LD_LIBRARY_PATH=/home/iisaka/.local/lib:${LD_LIBRARY_PATH}
```

次のファイルを用意します。このファイルがあると numpy と scipy はMKLを使ってビルドするようになります。
 $HOME/.numpy-site
```
 [mkl]
 library_dirs = /home/iisaka/.local/lib
 include_dirs = /home/iisaka/.local/include
 mkl_libs = mkl_rt
 lapack_libs =
 extra_link_args = -Wl,--rpath=/home/iisaka/.local/lib -Wl,--no-as-neede -lmkl_rt -ldl -lpthread -lm
```

先にnumpy や scipy のビルドに必要なモジュールをインストールしておきます。
 bash
```
 $ pip install cython, pybind11, pythran
```

ここで、mumpy のコンパイル済みの Weel パッケージを作成します・

 bash
```
 $ pip wheel --no-binary :all: numpy
```

 bash
```
 $ pip install ./numpy-*.whl
```

今度は、scipy も MKL を使ってビルドしてみます。
 bash
```
 $ pip wheel --no-deps --no-binary :all: scipy
```

 bash
```
 $ pip install ./scipy-*.whl
```

次回以降、numpy と scipy を再インストールする場合は、この wheel パッケージを直接指示するだけでOKです。
あるいは、次のようなディレクトリに保存しておいて、このディレクトリを探すようにすればよいでしょう。

 bash
```
 $ mkdir $HOME/cache/pypi
 $ mv numpy-*.whl scipy-*.whl $HOME/cache/pypi
 $ pip install --no-index --find-links $HOME/cache/pypi numpy
```

インストールが終わったら、mumpy/scipy がビルドされている環境を確認しておきましょう。
blas_mkl_info や lapck_mkl_infp が定義されていればOKです。

 bash
```
 $ python -c 'import numpy ; numpy.show_config()'
 blas_mkl_info:
     libraries = ['mkl_rt', 'pthread']
     library_dirs = ['/home/iisaka/.local/lib']
     define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
     include_dirs = ['/home/iisaka/.local/include']
     extra_link_args = ['-Wl,--rpath=/home/iisaka/.local/lib', '-Wl,--no-as-neede', '-lmkl_rt', '-ldl', '-lpthread', '-lm']
 blas_opt_info:
     libraries = ['mkl_rt', 'pthread']
     library_dirs = ['/home/iisaka/.local/lib']
     define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
     include_dirs = ['/home/iisaka/.local/include']
     extra_link_args = ['-Wl,--rpath=/home/iisaka/.local/lib', '-Wl,--no-as-neede', '-lmkl_rt', '-ldl', '-lpthread', '-lm']
 lapack_mkl_info:
     libraries = ['mkl_rt', 'pthread']
     library_dirs = ['/home/iisaka/.local/lib']
     define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
     include_dirs = ['/home/iisaka/.local/include']
     extra_link_args = ['-Wl,--rpath=/home/iisaka/.local/lib', '-Wl,--no-as-neede', '-lmkl_rt', '-ldl', '-lpthread', '-lm']
 lapack_opt_info:
         libraries = ['mkl_rt', 'pthread']
         library_dirs = ['/home/iisaka/.local/lib']
         define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
         include_dirs = ['/home/iisaka/.local/include']
         extra_link_args = ['-Wl,--rpath=/home/iisaka/.local/lib', '-Wl,--no-as-neede', '-lmkl_rt', '-ldl', '-lpthread', '-lm']
```


 bash
```
 $ python -c "import scipy; scipy.show_config()"
 lapack_mkl_info:
     libraries = ['mkl_rt', 'pthread']
     library_dirs = ['/home/iisaka/.local/lib']
     define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
     include_dirs = ['/home/iisaka/.local/include']
     extra_link_args = ['-Wl,--rpath=/home/iisaka/.local/lib', '-Wl,--no-as-neede', '-lmkl_rt', '-ldl', '-lpthread', '-lm']
 lapack_opt_info:
     libraries = ['mkl_rt', 'pthread']
     library_dirs = ['/home/iisaka/.local/lib']
     define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
     include_dirs = ['/home/iisaka/.local/include']
     extra_link_args = ['-Wl,--rpath=/home/iisaka/.local/lib', '-Wl,--no-as-neede', '-lmkl_rt', '-ldl', '-lpthread', '-lm']
 blas_mkl_info:
     libraries = ['mkl_rt', 'pthread']
     library_dirs = ['/home/iisaka/.local/lib']
     define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
     include_dirs = ['/home/iisaka/.local/include']
     extra_link_args = ['-Wl,--rpath=/home/iisaka/.local/lib', '-Wl,--no-as-neede', '-lmkl_rt', '-ldl', '-lpthread', '-lm']
 blas_opt_info:
     libraries = ['mkl_rt', 'pthread']
     library_dirs = ['/home/iisaka/.local/lib']
     define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
     include_dirs = ['/home/iisaka/.local/include']
     extra_link_args = ['-Wl,--rpath=/home/iisaka/.local/lib', '-Wl,--no-as-neede', '-lmkl_rt', '-ldl', '-lpthread', '-lm']
```


### グローバル変数へのアクセスを減らす
スクリプトを記述するとき、問題が簡単であればあるほど、少ないコードを単純に記述しやすいものです。
例えば、コマンドラインで指定したCSVファイルを読み出すというような場合では、
次のように書いてしまいがちです。

 optimize_local_vs_global1.py
```
 import sys 
 import csv 
   
 with open(sys.argv[1]) as f: 
     for row in csv.reader(f): 
         data = ''.join(row)
```

Python であまり知られていないことのひとつに、グローバル空間に定義されたコードは、関数として定義したコードよりも遅くなります。
この速度の違いは、ローカル変数とグローバル変数の実装が影響していて、ローカル変数への操作はグローバル変数への操作よりも高速に動作します。
したがって、上記のような場合でも、コードを関数にするだけで、プログラムの実行を高速化することができます。

optimize_local_vs_global2.py
```
 import sys 
 import csv 
   
 def main(filename): 
     with open(filename) as f: 
         for row in csv.reader(f): 
             data = ''.join(row)
   
 main(sys.argv[1]) 
```


 bash
```
 $ time python optimize_local_vs_global1.py sample.csv
 
 real    0m0.109s
 user    0m0.047s
 sys 0m0.030s
 
 $ time python optimize_local_vs_global2.py sample.csv
 
 real    0m0.054s
 user    0m0.036s
 sys 0m0.013s
```

もっとも、この程度の行数ではほとんど誤差のようなレベルですね。
重要なことはループ処理の中でグローバル変数をアクセスしないようにするということです。

### アトリビュート参照をしないようにする
モジュールの関数やオブジェクトのアトリビュートを参照するときにドット( `.` ) 表記を使います。
 optimized_attr_reference1.py
```
 import math
 
 def compute_roots(nums):
     result = []
     for n in nums:
         result.append(math.sqrt(n))
     return result
 
 nums = range(1000000)
 for n in range(100):
     r = compute_roots(nums)
```

これを、次のようにローカル変数に変えるだけで高速化されます。
 optimized_attr_reference2.py
```
 from math import sqrt
 
 def compute_roots(nums):
     result = []
     result_append = result.append
     for n in nums:
         result_append(sqrt(n))
     return result
```

理由は、ドット（ `.` )表記では内部的に辞書検索が発生していて、特にループ内部で繰り返し使われると影響が積み重なってゆくからです。
インポートの方法を変えることと、メソッド検索が発生しないように関数オブジェクトを変数にセットして利用すること、これだけで性能が改善します。

実はまだ改良の余地があります。はじめに説明しているように、グローバル変数へのアクセスはローカル変数に比べて遅くなります。そこで、 `math.sqrt()` をローカル変数となるようにすることで、さらに性能がよくなります。

 optimize_attr_reference3.py
```
 import math
 
 def compute_roots(nums):
     sqrt = math.sqrt
     result = []
     result_append = result.append
     for n in nums:
         result_append(sqrt(n))
     return result
```

 bash
```
 $ time python  optimize_attr_reference1.py
 
 real    0m1.904s
 user    0m1.865s
 sys 0m0.023s
 
 $ time python  optimize_attr_reference2.py
 
 real    0m1.217s
 user    0m1.182s
 sys 0m0.019s
 
 $ time python  optimize_attr_reference3.py
 
 real    0m1.122s
 user    0m1.091s
 sys 0m0.021s
```

ドット（ `.` )表記でアトリビュートを参照することは、クラス定義でも  `self.value` 
などのようにインスタンス変数へアクセスするときにも発生していします。
メソッドの中でループして何度も参照するようなときは、ローカル変数にする方が速くなります。

```
 class SlowerClass: 
     # ... 
     def method(self): 
         for x in range(1000): 
             func(self.value) 
             
 class FasterClass: 
     # ... 
     def method(self): 
         value = self.value 
         for x in range(1000): 
             func(value) 
```

### なるべくループをさせない
コードの記述方法を変えるだけでループをなくせる場合があります。
例えば、次のコードは２つのリストから重複しないユニークな要素を取り出すものです。
 IPython
```
 In [2]: # %load optimize_using_set.py 
    ...: a=[1,2,3,4,5,6,7,8,9] 
    ...: b=[9,8,7,6,5,4,3,2,1] 
    ...:  
    ...: def  func1(): 
    ...:     for x in a: 
    ...:         for y in b: 
    ...:             if x == y: 
    ...:                  yield (x) 
    ...: %timeit {c for c in func1()} 
    ...:                                                                           
 4.34 µs ± 35.6 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each) 
```

このようなコードはループでなくても、 `set()` を使うことで表現できます。
 IPYthon
```
 In [2]: # %load optimize_using_set2.py 
    ...: a=[1,2,3,4,5,6,7,8,9] 
    ...: b=[9,8,7,6,5,4,3,2,1] 
    ...:  
    ...: def func2(): 
    ...:     return set(a) & set(b) 
    ...:  
    ...: %timeit func2() 
    ...:                                                                           
 963 ns ± 37.1 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
 
```

### リスト内包表記を使う
単純な for 文を使うのではなくて、**リスト内包表記(list comprehension)** を使うと効率よく処理をすることができます。
 IPython
```
 In [1]: %%timeit 
    ...: old_list = [1,2,3,4] 
    ...: new_list = [] 
    ...: for item in old_list: 
    ...:     new_list.append(item + 1) 
    ...:                                                                           
 464 ns ± 29.7 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
```

Ipython
```
 In [1]: %%timeit 
    ...: old_list = [1,2,3,4] 
    ...: new_list = [] 
    ...: new_list = [item + 1 for item in old_list] 
    ...:  
    ...:                                                                           
 424 ns ± 3.2 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
```

### ループ内でif文を使う必要があるか検討する
ループ中でif文を使うと、当然のことならがループ回数だけ毎回条件判断が繰り返されてしまいます。
例外処理として扱うとこれを避けることができるようになります。

 Ipython
```
 list_of_strings = ['1', '2', '3', 'one', 'two', 'three', '4', '10']
 list_of_numbers = []
 for num in list_of_strings:
     if num.isdigit():
         list_of_numbers.append(int(num))
     else:
         print('String encountered')
```


```
 list_of_strings = ['1', '2', '3', 'one', 'two', 'three', '4', '10']
 list_of_numbers = []
 for num in list_of_strings:
     try:
         list_of_numbers.append(int(num))
     except:
         print('String encountered')
```

### zip()を使う
Python3.5 以降で’使用できる組み込み関数  `zip()` は複数のイテラブルオブジェクト（リストやタプルなど）の要素をまとめる関数です。
forループで複数のリストの要素を取得するときなどに使うと処理速度を向上することができます。

 IPython
```
 In [1]: %%timeit 
    ...: animals = ['aardvark', 'bee', 'cat', 'dog'] 
    ...: flowers = ['allium', 'bellflower', 'crocus', 'dahlia'] 
    ...: [(animals[i], flowers[i]) for i in range(min(len(animals), len(flowers)))]
    ...:                                                                           
 1.37 µs ± 296 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
 
 In [2]: %%timeit 
    ...: animals = ['aardvark', 'bee', 'cat', 'dog'] 
    ...: flowers = ['allium', 'bellflower', 'crocus', 'dahlia'] 
    ...: [(animal, flower) for animal, flower in zip(animals, flowers)] 
    ...:                                                                           
 890 ns ± 66.9 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
```


### 配列の先頭への挿入には deque を使う
 `array` 型や `list` 型 では先頭へのオブジェクトの挿入は非常に遅くなります。 
こうした場合は、 `collections` モジュールの  `deque` を使うようにします。

> Pythonのドキュメントから:
>  Deque とは、スタックとキューを一般化したものです
> (この名前は「デック」と発音され、これは「double-ended queue」の省略形です)。
> Deque はどちらの側からも appendとpopが可能で、スレッドセーフでメモリ効率がよく、どちらの方向からもおよそ O(1) のパフォーマンスで実行できます。

 Ipython
```
 import sys
 from array import array
 from benchmarker import Benchmarker
 from collections import deque
  
 n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000*1000
 print(n) 
 with Benchmarker(n, width=20) as bench:
     nay = []
     iay = array('I', [])
     day = deque()
  
     @bench("list")
     def _(bm):
         for i in range(n):
             nay.insert(0, i)
  
     @bench("array")
     def _(bm):
         for i in range(n):
             iay.insert(0, i)
  
     @bench("deque")
     def _(bm):
         for i in bm:
           day.appendleft( i )
```

### 計算結果をキャッシュする
次のコードはフィボナッチ数列のN番目の数字を求める問題を、再帰呼び出しで実装したものです。

```
 def fib(n):
     if n<2:
         return n
     return fib(n-1)+fib(n-2)
```

このコードは同じ計算を何度も実行します。つまり、 `fib(20)` は `fib(19)` と `fib(18)` を呼び出し、 その次に `fib(19)` は `fib(18)` と `fib(17)` を呼び出します。
その結果 `fib(18)` は2回呼び出されます。 少し考えると分かりますが、 `fib(17)` は3回、 `fib(16)` は5回…と呼び出されることになります。
Python 3の標準ライブラリ  `functools` の `lru_cache` を使うと計算結果がキャッシュされるため、このような重複した計算を実行せずに済みます。

Ipython
```
 In [2]: # %load optimize_using_cache1.py 
    ...: def fibo(n): 
    ...:     if n<2: 
    ...:         return n 
    ...:     return fibo(n-1)+fibo(n-2) 
    ...:  
    ...: from functools import lru_cache as cache 
    ...: @cache(maxsize=None) 
    ...: def fibo_cache(n): 
    ...:     if n<2: 
    ...:         return n 
    ...:     return fibo_cache(n-1)+fibo_cache(n-2) 
    ...:                                                                    
 In [3]: %timeit fibo(30)                                                   362 ms ± 32.7 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
 In [4]: %timeit fibo_cache(30)                                             104 ns ± 1.85 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
```

### 自分でコードを書く前に調べよう
まず間違いなく、自分でコードを書くよりも高速化されたライブラリを使う方が性能がよくなります。そのため、ライブラリへの知識はとても重要になります。

次のコードを比較してみましょう。
 Ipython
```
 import math
 import numpy as np
 
 def list_append(x):
     results = []
     for i in range(x):
         results.append(math.sqrt(i))
     return results
 
 def list_comp(x):
     results = [math.sqrt(i) for i in range(x)]
     return results
 
 def list_map(x):
     results = map(math.sqrt, range(x))
     return results
 
 def list_numpy(x):
     results = list(np.sqrt(np.arange(x)))
     return results
```

実行性能を比較してみましょう。
 IPython
```
 In [3]: x=10000                                                            
 In [4]: %timeit list_append(x)                                             
 1.75 ms ± 18.9 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
 
 In [5]: %timeit list_comp(x)                                               
 1.33 ms ± 42 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
 
 In [6]: %timeit list_map(x)                                                
 542 ns ± 12.6 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
 
 In [7]: %timeit list_numpy(x)                                              
 868 µs ± 24.4 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
```


### bottleneck を使ってみる
NumPy が提供している関数の演算処理をさらに高速化した、  `bottleneck` という拡張モジュールがあります。 
これを使うだけでも大幅な性能向上が期待できます。
ただし、欠点としては既存コードを書き換える必要があります。

 Ipython
```
 In [2]: # %load optimize_using_bottleneck1.py 
    ...: import numpy as np 
    ...: a = np.array([1, 2, np.nan, 4, 5]) 
    ...:  
    ...: %timeit np.nanmean(a) 
    ...:                                                                           
 33.7 µs ± 1.12 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
```

 IPython
```
 In [4]: # %load optimize_using_bottleneck2.py 
    ...: import numpy as np 
    ...: import bottleneck as bn 
    ...:  
    ...: a = np.array([1, 2, np.nan, 4, 5]) 
    ...: %timeit bn.nanmean(a) 
    ...:                                                                           
 249 ns ± 24.3 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each) 
```

 `bench()` を呼び出すと（時間は少しかかります）、NumPyと比較して何倍速くなったかを計測してくれます。
 Ipython
```
 In [5]: bn.bench()                                                                
 Bottleneck performance benchmark
     Bottleneck 1.3.2; Numpy 1.18.1
     Speed is NumPy time divided by Bottleneck time
     NaN means approx one-fifth NaNs; float64 used
 
               no NaN     no NaN      NaN       no NaN      NaN    
                (100,)  (1000,1000)(1000,1000)(1000,1000)(1000,1000)
                axis=0     axis=0     axis=0     axis=1     axis=1  
 nansum         28.8        0.7        1.9        1.0        2.6
 nanmean       107.6        1.2        1.5        2.8        2.3
 nanstd        171.3        1.4        1.8        2.3        2.6
 nanvar        164.3        1.3        1.7        2.1        2.4
 nanmin         18.6        0.5        0.5        1.0        1.1
 nanmax         18.1        0.5        0.4        1.0        1.1
 median        116.0        1.3        6.1        1.1        7.6
 nanmedian     122.4        5.6        6.4        5.6        6.3
 ss             12.5        0.7        0.7        1.0        1.0
 nanargmin      70.7        2.3        3.5        2.2        4.5
 nanargmax      65.4        2.1        3.4        1.9        4.2
 anynan         10.8        0.3       73.0        0.7       52.9
 allnan         15.9      186.1      169.6      132.3      116.6
 rankdata       47.4        1.3        1.3        2.3        2.3
 nanrankdata    51.2        1.5        1.5        2.5        2.5
 partition       3.9        1.1        1.3        1.0        1.3
 argpartition    3.6        1.2        1.4        1.1        1.5
 replace        12.3        1.6        1.6        1.9        2.5
 push         1009.8        5.3        7.1       11.4       11.1
 move_sum     2476.0       40.8      100.5      182.0      204.2
 move_mean    7015.0       68.3      121.6      279.6      252.0
 move_std    10110.5       95.5      252.1      383.7      264.7
 move_var     6487.2      116.7      119.2      277.0      259.2
 move_min      986.8       16.1       16.9       41.0       54.2
 move_max     1424.5       15.3       15.1       39.6       37.3
 move_argmin  2459.6       52.9       88.9       68.2      135.8
 move_argmax  2756.2       64.8       77.9       65.3      120.9
 move_median  2089.9      153.6      151.7      236.1      202.3
 move_rank     771.5        1.2        1.5        3.8        1.4
 
```

### Cython を使ってみる
拡張モジュールCython はPythonとほぼ同一のコードをC/C++でネィティブコンパイルして高速実行することができます。
cython の使い方には少し手間が必要になるのですが、jupyter や jupyterlab、IPython では簡単に cython を使用することができます。

はじめに ` %load_ext ` のマジックコードで Cython を使えるようにしておきます

 IPython
```
 %load_ext Cython
```

 Ipython
```
 def fibo_python(n):
     a, b = 0, 1
     for i in range(n):
         a, b = a + b, a
     return a
```

次に、マジックコマンド `%%cython` を付加したコードです。
 IPython
```
 %%cython
 def fibo_cython(n):
     a, b = 0, 1
     for i in range(n):
         a, b = a + b, a
     return a
```

これに、変数  `n` に型指定を与えたコードです。
 Ipython
```
 %%cython
 def fibo_typed_cython(int n):
     a, b = 0, 1
     for i in range(n):
         a, b = a + b, a
     return a
```

Cython で使える  `cdef` 文を使って、全ての変数に型指定を行ったコードです。
 Ipython
```
 %%cython
 def fibo_all_typed_cython(int n):
     cdef int a,b,i
     
     a, b = 0, 1
     for i in range(n):
         a, b = a + b, a
     return a
```

実行性能を比較してみましょう。
 IPython
```
 In [6]: n=5000                                                             
 In [7]: %timeit fibo_python(n)                                             
 744 µs ± 37.9 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
 
 In [8]: %timeit fibo_cython(n)                                             
 571 µs ± 36.4 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
 
 In [9]: %timeit fibo_typed_cython(n)                                       
 474 µs ± 22 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
 
 In [10]: %timeit fibo_all_typed_cython(n)                                  
 1.69 µs ± 21.7 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
```

なにも変更を加えずにマジックコード  `%%cython` を与えただけでもかなり高速ですが、 使用する変数の型指定を行うと圧倒的に処理が高速になります。

### numba を使ってみる
拡張モジュール  `numba` は Anaconda Python をリリースしている Continuum Analytics, Inc が開発した **JIT(Just In Time)コンパイラ** という技術を利用したPythonライブラリです。

 `numba` の使い方は驚くほど簡単で、numba モジュールをインポートして、 デコレータ `@jit` を関数の前に記述するだけです。

 IPython
```
 In [2]: # %load optimize_using_numba.py 
    ...: from numba import jit 
    ...:  
    ...: def fibo_python(n): 
    ...:     a, b = 0, 1 
    ...:     for i in range(n): 
    ...:         a, b = a + b, a 
    ...:     return a 
    ...:  
    ...: @jit 
    ...: def fibo_numba(n): 
    ...:     a, b = 0, 1 
    ...:     for i in range(n): 
    ...:         a, b = a + b, a 
    ...:     return a 
```

実行性能を比較してみましょう。
 IPython                                                              
```
 In [3]: n=5000                                                             
 In [4]: %timeit fibo_python(n)                                              
 676 µs ± 37.7 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
 
 In [5]: %timeit fibo_numba(n)                                               
 2.55 µs ± 1.3 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

### アルゴリズムを検証する
例えば、自然数が順にならんだ配列があり、その総和を求めたいとします。

[$ \sum_{k=1}^{n}k = 1 + 2 + \cdots + n]

こうしたとき、闇雲に次のようなコードを書いてはいけません。


```
 n = 1_000_000
 result = 0
 for i in range(1, n+1):
     result += i
```

この場合、よく知られた自然数の和の公式を使用するべきです。

[$ \sum_{k=1}^{n}k = \frac{n(n+1)}{2}]


```
 n = 1_000_000
 result = (n * (n + 1))/2
```

科学技術計算プログラミングでの要点は[# SMASH] だと言われています。これは、次の項目の頭文字を並べたものです。

- [# S]cience
- [# M]odeling
- [# A]lgorithm
- [# S]oftware
- [# H]ardware

また、これらには重要度がそのまま表現されています。つまり、ソフトウェアのないハードウェアは意味がない、どんなに凝ったサブルーチンよりも優れたアルゴリズムの方が効率的な結果が得られる、といった示唆が含まれています。
さらには、高速化するために分散処理を行う場合では、HPCクラスタシステムやHdoop分散クラスタ、Kubernetesクラスタといったプラットフォームがハードウェアに該当します。このため、並列プログラミングや分散処理プログラミングの理解と習得が非常に重要だということにもなります。

### 高速化のコツ
ループ中での条件判断を避けたりなど、やりたいことの処理方法を少し検討するだけでも速度向上が得られることもあります。

numba や cython で高速化できる部分というのは演算処理の部分だけです。 メモリアクセスやディスクI/Oでのデータ読み込み待ちには殆ど効果がありません。

また、1回しか呼ばれない関数を10%高速化するより、100,000回呼ばれる関数を1%高速化するほうが 全体としては性能向上となる場合があることを理解しましょう。

つまり、ボトルネックとなっている箇所と原因を理解したうえで、適切な対応をするということが非常に重要です。

## 参考
- [Python チュートリアル：プロファイリングツール]
- [bottleneck: Fast NumPy array functions written in C ](https://github.com/kwgoodman/bottleneck)
- [numba project http://numba.pydata.org/]
- [cython project ](https://cython.org/)
- [Benchmaker: Step by Step tutorial ](https://pythonhosted.org/Benchmarker/)
- [Premature Optimization http://wiki.c2.com/?PrematureOptimization]




