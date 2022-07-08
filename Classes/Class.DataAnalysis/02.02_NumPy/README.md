NumPy を使ってみよう
=================
![](https://gyazo.com/476cf73b42e0261bbcf227f86464aa92.png)

## NumPyについて
NumPy は Python を使って数値計算をするときに非常に便利なモジュールで、
次のような特徴があります。

- 処理速度が高速で、多彩な数学関数が提供されている
- 配列の扱い方が柔軟になり、行列計算が簡単に記述できる
- アルゴリズムを実装するときのコードが簡潔で読みやすい

NumPy で使用できる応用範囲を次にあげておきます。

- 効率的な配列処理(ndarray)
- [数学関数 ](https://docs.scipy.org/doc/numpy/reference/routines.math.html)
- [線形代数 https://docs.scipy.org/doc/numpy/reference/routines.linalg.html]、[行列演算 ](https://docs.scipy.org/doc/numpy/reference/routines.matlib.html)
- [フーリエ変換 ](https://docs.scipy.org/doc/numpy/reference/routines.fft.html)
- [統計計算 ](https://docs.scipy.org/doc/numpy/reference/routines.statistics.html)
- [ファイナンス計算 ](https://docs.scipy.org/doc/numpy/reference/routines.financial.html)


Python のディストリビューションは複数ありますが、
Anaconda Python と Intel Distribution for Python (Intel Compiler にも含まれています) は、
Intel MKL(Math Kernel Library) を使ってビルドされているため、他のものよりも性能が優れているのでお勧めします。（[Python ベンチマークテスト　](https://software.intel.com/en-us/distribution-for-python/benchmarks)）

## インストール
拡張モジュールなので次のようにインストールします。
 bash condaの場合
```
 $ conda install numpy
 bash pipの場合
```
 $ pip install  numpy
```

## NumPy の詳細
### データ型
NumPy では次のデータ型(Data Type)が定義されています。
配列生成時などでは、 `dtype=numpy.int32` というように指定します。
 NumPy で使用できるデータ型

| NumPy | データ型  | 説明 |
|:--|:--|:--|
| bool_ | ブール型 | True / False 　1 byte に格納 |
| int_ | デフォル整数型 | int64、機種依存でint32 |
| intc | C言語と同じ整数型 | int64、機種依存でint32 |
| intp | インデックス用整数 | C言語のssize_t, int64, int32 |
| int8 | バイト | -128 ～ 127 |
| int16 | 整数型 | -32768 ～ 32767 |
| int32 | 整数型 | -2147483648 ～ 2147483647 |
| int64 | 整数型 | -9223372036854775808 ～ 9223372036854775807 |
| uint8 | 8bit符号なし整数型 | 0 ～ 255 |
| uint16 | 16bit符号なし整数型 | 0 ～ 65535 |
| uint32 | 32bit符号なし整数型 | 0 ～ 4294967295 |
| uint64 | 64bit符号なし整数型 | 0 ～ 18446744073709551615 |
| float_ | 倍精度浮動小数点数型 | float64 と同じ |
| float16 | 半精度浮動小数点数型 | 符号 1bit, 指数部 5bit, 仮数部 10bit |
| float32 | 単精度浮動小数点数型 | 符号 1bit, 指数部 8bit, 仮数部 23bit |
| float64 | 倍精度浮動小数点数型 | 符号 1bit, 指数部 11bit, 仮数部 52bit |
| complex_ | 128ビット複素数型 | complex128 と同じ |
| complex64 | 64ビット複素数型 | 虚部/実部が各々float32で表される複素数型 |
| complex128 | 128ビット複素数型 | 虚部/実部が各々float64で表される複素数型 |
| str | ユニコード文字列型 |  |
| void | Rawデータ型 |  |

### 複合データ型
Pythonの `array` は１つのデータ型しか保持できませんでしたが、 `NumPy` では異なるデータ型の要素を組み合わせた複合データ型を `dtype()` で定義することができます。

Ipython
```
 In [2]: # %load numpy_datatype.py 
    ...: import numpy as np 
    ...:  
    ...: dt_1 = np.dtype(np.int32) 
    ...: dt_2 = np.dtype('i4') 
    ...: dt_3 = np.dtype([('age',np.int8)]) 
    ...: dt_4 = np.dtype("i4, (2,3)f8, f4") 
    ...:  
    ...: a = np.array([(10,),(20,),(30,)], dtype = dt_3) 
    ...: employee = np.dtype([('name','S20'), ('age', 'i1'), ('salary', 'f4')]) 
    ...:  
    ...: print(dt_1) 
    ...: print(dt_2) 
    ...: print(dt_3) 
    ...: print(dt_4) 
    ...:  
    ...: print(a.dtype) 
    ...: print(employee) 
    ...:                                                                           
 int32
 int32
 [('age', 'i1')]
 [('f0', '<i4'), ('f1', '<f8', (2, 3)), ('f2', '<f4')]
 [('age', 'i1')]
 [('name', 'S20'), ('age', 'i1'), ('salary', '<f4')]
```

はじめの  `dt_1` は単純に  `np.int32` を与えているだけです。
次の、 `dt_2` は  `i1` として `dtype()` に与えています。これは、 `np.int32` を１バイトという意味になります。
 `dt_3` では、 `i1` のデータ型に `age` という名前をつけています。
これを使って配列を生成したものが、 `a` です。
 `dt_4` と `employee` が複合型のデータを定義したものです。
 `dt_4` は はじめの `f0` と名前づけされたフィールドには `np.int32` 、同様に `f1` フィールドには、 `np.float64` のデータが2x3の配列、 `f2` フィールドには `np.float64` で構成されたデータ型となります。
最後の `employee` では、フィールドに名前をつけています。
このとき、 `<f4` とあるのはリトルエンディアンで表現された `float64` 型を表らわしたものです。エンディアン表記は、ビッグエンディアン（ `>` ） とリトルエンディアン（  `<` ） の２つになります。インテル社が主流となっている昨今のCPUは、リトルエンディアンとなります。

([Wikipedia: エンディアン ](https://ja.wikipedia.org/wiki/%E3%82%A8%E3%83%B3%E3%83%87%E3%82%A3%E3%82%A2%E3%83%B3))
> **ビッグエンディアンとリトルエンディアン**
> 16進法表記で、1234ABCD の1ワードが4バイトのデータを、
> バイト毎に上位側から「12 34 AB CD」のように並べる順序はビッグエンディアン、
> 下位側から「CD AB 34 12」のように並べる順序はリトルエンディアン

 `dtype()` に与えることができる、型指定子は次のものが使えます。
 dtype()での型指定子

| 指定子 | 型 | 説明 |
|:--|:--|:--|
| b | ブール型 | True/False |
| i | 符号付き整数 | i1(int8), i2(int16), i4(int32), i8(int64) |
| u | 符号なし整数 | u1(uint8), u2(uint16), u4(uint32), u8(uint64) |
| f | 不動所数点 | f2(float16), f4(float32), f8(float64) |
| c | 複素浮動小数点 | c8(complex64), c16(complex128) |
| m | timedelta |  |
| M | datetime |  |
| O | Pythonオブジェクト |  |
| S | string(バイト列) | NULL(ゼロ）終端の文字列、非推奨 |
| a | string(バイト列) | NULL(ゼロ）終端の文字列、非推奨 |
| U | Unicode文字列 |  |
| V | rawデータ | void |

### 配列
Python の  `array` 型や `list` 型では、２つのオブジェクトのそれぞれの要素ごとに演算をしたいときは次のようなコードになります。
 IPython
```
 In [2]: # %load sample_add_array.py 
    ...: import array 
    ...:  
    ...: a = array.array('i', [1,2,3,4,5]) 
    ...: b = array.array('i', [6,7,8,9,10]) 
    ...: for i in range(5): 
    ...:     print(a[i]+b[i]) 
    ...:  
    ...: print(a + b) 
    ...:                                                                           
 7
 9
 11
 13
 15
 array('i', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
```

これが、 `numpy` を使うとつぎのように簡単に記述できます。
 IPython
```
 n [2]: # %load sample_add_numpy.py 
    ...: import numpy as np 
    ...:  
    ...: a = np.array([1,2,3,4,5]) 
    ...: b = np.array([6,7,8,9,10]) 
    ...: print(a + b) 
    ...:                                                                           
 [ 7  9 11 13 15]
```

python の  `array` 型 や  `list` 型では、演算子 `+` はオブジェクトの連結になりますが、
 `numpy` では、それぞれの要素ごとに演算した結果を返します。

要素ごとに演算するためにループを使うと、次元が多くなればなるほど、ループがネストしてゆき、どんどん速度も遅くなっていきます。もちろん、コードが判読性が失われていきます。

 `NumPy` で多次元配列を扱う `ndarray` クラスは、Python の  `array` 型と同じように扱えるインスタンオブジェクトを生成します。
要素ごとの演算が可能で、多次元計算が簡潔に記述できます。
線形代数学では、１次元配列を**ベクトル(Vector)**、２次元配列を**行列(Matrix)** と呼びます。

### 配列の生成方法
 `NumPy` にはいくつかの配列生成方法があります。

よく使用されるゼロ化する処理の例です。
 Ipython
```
 In [2]: # %load numpy_create_array1.py 
    ...: import numpy as np 
    ...:  
    ...: a = np.array([0]*5) 
    ...: b = np.zeros(5, dtype=np.int) 
    ...:  
    ...: c = np.zeros((2,2)) 
    ...:                                                                           
 In [3]: a                                                                 Out[3]: array([0, 0, 0, 0, 0])
 
 In [4]: b                                                                 Out[4]: array([0, 0, 0, 0, 0])
 
 In [5]: c                                                                 Out[5]: 
 array([[0., 0.],
        [0., 0.]])
```

 `a` と  `b` は同じ結果になりますが、 `zeros()` を使う方が多次元配列の初期化が簡単で、処理速度が速くなります。
 IPython
```
 In [3]: %timeit a = np.array([0]*100000)                                          
 7.08 ms ± 35.3 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
 
 In [4]: %timeit b = np.zeros(100000,dtype=np.int)                                 
 21.4 µs ± 1.72 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
 
```

>  `%timeit` はIPython(あるいはJupyter Notebook)で使用できる
>   時間計測のためのマジックコマンドです。

ただし、 `a` の書式ではリスト内包表記が使えるので、より複雑な初期化を行うことができます。

```
 In [1]: import numpy as np                                                        
 In [2]: np.array([i if i%2 ==0 else 0 for i in range(10)])                Out[2]: array([0, 0, 2, 0, 4, 0, 6, 0, 8, 0])
```


 `zeros()` は `array` の要素をすべてゼロにするものでした。
これに対して、  `ones()` は全ての要素を１にし、 `full()` は指定した値で埋め尽くします。

Ipython
```
 In [2]: # %load numpy_create_array2.py 
    ...: import numpy as np 
    ...:  
    ...: d = np.ones((2,3)) 
    ...: e = np.full((2,3), 4) 
    ...:  
    ...: print(f'\n np.ones((2,3)):\n{d}') 
    ...: print(f'\n np.full((2,3), 4):\n{e}') 
    ...:                                                                           
 
  np.ones((2,3)):
 [[1. 1. 1.]
  [1. 1. 1.]]
 
  np.full((2,3), 4):
 [[4 4 4]
  [4 4 4]]
```

 `eye()` は指定した次元の**単位行列(identity matrix)** を作成します。
単位行列とは次のように対角成分に 1 が並び、他は全て 0 となる行列をいいます。

[$ \left( \begin{array}{cc} 1 & 0 & \cdots & 0\\ 0 & 1 & \cdots & 0\\ \vdots & \vdots & \ddots & \vdots\\ 0 & 0 & \cdots & 1\\ \end{array} \right)]

 `np.random.random()` では、すべての要素を１を超えない乱数で埋め尽くします。
 IPython
```
 In [2]: # %load numpy_create_array3.py 
    ...: import numpy as np 
    ...:  
    ...: f = np.eye(3) 
    ...: g = np.random.random((2,3)) 
    ...:                                                                   
 In [3]: f                                                                 Out[3]: 
 array([[1., 0., 0.],
        [0., 1., 0.],
        [0., 0., 1.]])
 
 In [4]: g                                                                 Out[4]: 
 array([[0.64434419, 0.79095428, 0.7467826 ],
        [0.32752408, 0.01371972, 0.34652259]])
```

 `arange()` は引数で与えた数のサイズで配列を生成します。
 `empty()` は引数で与えた数のサイズで配列を生成します。
 `empty_like()` は引数で与えた配列と同じ大きさの配列を返します。
他の関数は何らかの初期化が行われますが、 `empty()` と `emty_like()` はメモリ領域を確保するだけで、要素はそのときのメモリの状態により決まります。
 IPython
```
 In [2]: # %load numpy_create_array4.py 
    ...: import numpy as np 
    ...:  
    ...: a = np.arange(5) 
    ...: b = np.empty(5) 
    ...:  
    ...: c = np.eye(3) 
    ...: d = np.empty_like(c) 
    ...:                                                                           
 In [3]: a                                                                 Out[3]: array([0, 1, 2, 3, 4])
 
 In [4]: b                                                                 Out[4]: 
 array([ 1.28822975e-231, -2.00389378e+000,  1.48219694e-323,
         0.00000000e+000,  0.00000000e+000])
 
 In [5]: c                                                                 Out[5]: 
 array([[1., 0., 0.],
        [0., 1., 0.],
        [0., 0., 1.]])
 
 In [6]: d                                                                 Out[6]: 
 array([[ 1.28822975e-231,  1.28822975e-231, -3.95252517e-323],
        [ 0.00000000e+000,  2.12199579e-314,  0.00000000e+000],
       
```

NumPy が提供している配列を生成する関数を一覧しておきます。

-  `numpy.arange()` ： 指定した数の配列を生成する、要素は `range()` の内容と同じ
-  `numpy.zeros()` ； 指定した形状の配列を生成して、ゼロで初期化
-  `numpy.zeros_like()` ：与えた配列と同じ形状の配列を生成して、ゼロで初期化
-  `numpy.ones()` ：指定した形状の配列を生成して、１で初期化する
-  `numpy.ones_like()` ：与えた配列と同じ形状の配列を生成して、１で初期化
-  `numpy.full()` ：指定した形状の配列を生成して、与えた値で初期化
-  `numpy.full_like()` ：与えた配列と同じ形状の配列を生成して、与えた値で初期化
-  `numpy.eye()` ：単位行列を生成
-  `numpy.identity()` ：単位行列を生成
-  `numpy.matrix()` ：２次元配列（行列）を生成
-  `numpy.linspace()` ：指定した範囲の数列を含む配列を生成
-  `numpy.logspace()` ：指定した範囲の等比数列を含む配列を生成
-  `numpy.geomspace()` ：指定した範囲の等比数列を含む配列を生成
-  `numpy.diag()` ：対角行列の生成
-  `numpy.fromfunction()` ：指定した形状の配列を生成して、関数を呼び出して初期化
-  `numpy.empty()` ：指定した形状の配列を生成する。初期化はしない
-  `numpy.empty_like()` ：与えた配列と同じ形状の配列を生成する。初期化はしない

### 配列要素の抽出
Pythonの `array` 型オブジェクトがデータ型固定のシーケンスで `list` 型オブジェクトと同じ操作ができるように、 `NumPy` も配列のスライシングやインデックスといった操作ができます。

 IPython
```
 In [2]: a = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])              
 In [3]: b = a[:2, 1:3]                                                    
 In [4]: a                                                                 Out[4]: 
 array([[ 1,  2,  3,  4],
        [ 5,  6,  7,  8],
        [ 9, 10, 11, 12]])
 
 In [5]: b                                                                 Out[5]: 
 array([[2, 3],
        [6, 7]])
 
 In [6]: a[0, 1]                                                           Out[6]: 2
 
 In [7]: b[0, 0] = 99                                                      
 In [8]: b                                                                 Out[8]: 
 array([[99,  3],
        [ 6,  7]])
 
 In [9]: a[0, 1]                                                           Out[9]: 99
 
 In [10]: a                                                                Out[10]: 
 array([[ 1, 99,  3,  4],
        [ 5,  6,  7,  8],
        [ 9, 10, 11, 12]])
```
この例では、はじめに3x4(行ｘ列) の行列 `a` を作っています。
この行列からスライシングで０〜１行目( `:2` ) の、１〜２列目( `1:3` )のデータを取り出して、2x2の行列からなる  `array` オブジェクト `b` を作成しています。

 `a[0, 1]` と  `b[0, 0]` は同じオブジェクトになることに注意してください。

### 配列の形状を知る方法

配列をスライシングすることで、任意部分のデータにアクセスできます。
このとき、2つの方法があります。

- 整数インデックスとスライスを混在させる
  - より低いランクの配列が生成される
　スライスのみを使用する
　	元の配列と同じランクの配列が生成される

#### ランク(rank)
例えば、行列 A の階数は、A の列空間の次元に等しく、また A の行空間の次元とも等しくなります。行列を簡約化し、 主成分の数を数えることでランクを求めることができます。

 IPython
```
 In [2]: a = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])                In [3]: b = a[1, :]                                                       In [4]: c = a[1:2, :]                                                             
 In [5]: b                                                                 Out[5]: array([5, 6, 7, 8])
 
 In [6]: c                                                                 Out[6]: array([[5, 6, 7, 8]])
 
 In [7]: b.shape                                                           Out[7]: (4,)
 
 In [8]: c.shape                                                           Out[8]: (1, 4)
 
```
配列 `b` は `a` からインデックスとスライスを混在させて抽出しているため、ランクが下がり、配列として表示されます。
配列 `c` はスライシングだけで抽出しているので、ランクは `a` と同じに行列として表示されます。

ランクを知るためには 次のように実行します。

```
 In [9]: np.linalg.matrix_rank(a)                                         Out[9]: 2
```

 `shape` を参照すると、その配列の形状を知ることができます。
 `shape` は(行数、列数) のタプルはセットされています。

 `b.shape` は  `(4,)` なので列がなくて４要素の１次元配列、 `c.shape` は  `(1,4)` だから1行４列の行列ということがわかります。 `c.share[0]` や  `c.shape[1]` としてタプルの要素にアクセスすると、行や列だけの形状を知ることができます。

 `shape` アトリビュートにセットした値で、行列の形状を変えることもできます。
 IPyhton
```
 In [10]: b                                                                Out[10]: array([5, 6, 7, 8])
 
 In [11]: b.shape = (2,2)                                                  In [12]: b                                                                Out[12]: 
 array([[5, 6],
        [7, 8]])
```

 `reshape()` メソッドは `shape` アトリビュートに値をセットすることと同じく、配列の形状を変えることができます。

 IPython
```
 In [2]: a = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])                In [3]: b = a[1, :]                                                       In [4]: b                                                                 Out[4]: array([5, 6, 7, 8])
 
 In [5]: b = a[1, :].reshape(2,2)                                          In [6]: b                                                                 Out[6]: 
 array([[5, 6],
        [7, 8]])
```

### ndimで配列の次元数を知る
 `ndim` アトリビュートを参照すると、その配列の次元数を知ることができます。
 IPython
```
 In [7]: a = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])                In [8]: b = a[1, :]                                                               
 In [9]: b.ndim                                                            Out[9]: 1
 
 In [10]: a.ndim                                                           Out[10]: 2
```

### 整数配列を使った抽出(Integer Indexing)

スライスを使用して配列にインデックスを作成すると、返される配列は常に元の配列の部分配列になります。 整数配列のインデックスでは、別の配列のデータを使用して任意の配列を構築することができます。 

 IPython
```
 In [2]: # %load numpy_integer_indexing.py 
    ...: import numpy as np 
    ...:  
    ...: a = np.array([[1,2], [3, 4], [5, 6]]) 
    ...:  
    ...: b = np.array([a[0, 0], a[1, 1], a[2, 0]]) 
    ...: c = a[[0, 1, 2], [0, 1, 0]] 
    ...:
    ...: d = np.array([a[0, 1], a[0, 1]]) 
    ...: e = a[[0, 0], [1, 1]] 
    ...:                                                                           
 
 In [3]: a                                                                 Out[3]: 
 array([[1, 2],
        [3, 4],
        [5, 6]])
 
 In [4]: b                                                                 Out[4]: array([1, 4, 5])
 
 In [5]: c                                                                 Out[5]: array([1, 4, 5])
 
 In [6]: d                                                                 Out[6]: array([2, 2])
 
 In [7]: e                                                                 Out[7]: array([2, 2])
```

 `b` と  `c` は同じ結果となります。 `b` は `a` の要素をインデックスで抽出したものから `array` オブジェクトを作っています。整数配列のインデックスを使うと、同じことを簡潔に記述することができます。

> 配列Aがあるとき、
>         A［A［行index,列index］,A［行index,列index］,... ］
> これと同じ動作は、次のように記述できます。
>          A［［行indexのリスト］, ［列indexのリスト］］

配列の要素をインデックスを要素とする配列を使って抽出できるわけです。
 IPython
```
 In [2]: # %load numpy_integer_indexing2.py 
    ...: import numpy as np 
    ...:  
    ...: a = np.array([[1,2,3], [4,5,6], [7,8,9], [10, 11, 12]]) 
    ...: b = np.array([2, 1, 0, 1]) 
    ...: c = np.arange(4) 
    ...: d = a[c, b]         # a[[0,1,2,3], [2,1,0,1]
    ...: e = a[c, b] + 10 
    ...:                                                                           
 
 In [3]: a                                                                 Out[3]: 
 array([[ 1,  2,  3],
        [ 4,  5,  6],
        [ 7,  8,  9],
        [10, 11, 12]])
 
 In [4]: b                                                                 Out[4]: array([2, 1, 0, 1])
 
 In [5]: c                                                                 Out[5]: array([0, 1, 2, 3])
 
 In [6]: d   # a[[0,1,2,3], [2,1,0,1]
 Out[6]: array([ 3,  5,  7, 11])
 
 In [7]: e   # a[[0,1,2,3], [2,1,0,1] + 10
 Out[7]: array([13, 15, 17, 21])
```

### 条件式を使った抽出(Boolean Indexing)
条件式に合致する要素を抽出することができます。
 IPython
```
 In [2]: # %load numpy_boolean_indexing.py 
    ...: import numpy as np 
    ...:  
    ...: a = np.array([[1,2], [3, 4], [5, 6]]) 
    ...: b = (a > 2) 
    ...: c = a[b] 
    ...: d = a[a > 2] 
    ...:                                                                           
 
 In [3]: a                                                                 Out[3]: 
 array([[1, 2],
        [3, 4],
        [5, 6]])
 
 In [4]: b                                                                 Out[4]: 
 array([[False, False],
        [ True,  True],
        [ True,  True]])
 
 In [5]: c                                                                 Out[5]: array([3, 4, 5, 6])
 
 In [6]: d                                                                 Out[6]: array([3, 4, 5, 6])
```

 `b` は  `a` の各要素が２以上かをチェックした真偽値が格納された配列です。
 `c` は  `a` のインデックスとして `b` を与えると、 `True` の要素だけが抽出されます。

### 配列どうしの演算
配列どうしを演算するときは、演算子を使う方法とメソッドを呼び出す方法があります。
通常は演算子を使って計算するだけでよいでしょう。

 IPython
```
 In [2]: # %load numpy_math1.py 
    ...: import numpy as np 
    ...:  
    ...: x = np.array([[1,2],[3,4]], dtype=np.float64) 
    ...: y = np.array([[5,6],[7,8]], dtype=np.float64) 
    ...:  
    ...: a1 = x + y 
    ...: a2 = np.add(x, y) 
    ...:  
    ...: b1 = y - x 
    ...: b2 = np.subtract(y, x) 
    ...:  
    ...: c1 = x * y 
    ...: c2 = np.multiply(x, y) 
    ...:  
    ...: d1 = x / y 
    ...: d2 = np.divide(x, y) 
    ...:
    ...: e1 = y % x 
    ...: e2 = np.fmod(y, x) 
    ...:  
    ...: f1 = y ** x 
    ...: F2 = np.power(y, x) 
                                                                               
```
注意しておいてほしいことは、 `array` オブジェクトでは、演算子 `*` は要素ごとの乗算で、行列の乗算ではありません。（補足説明１も参照のこと）

行列の乗算をする場合は、 `dot()` を使って処理します。
 `dot()` は、numpyモジュールの関数と、 `array` オブジェクトのメソッドとしても提供されています。

> 補足説明１：　numpy.ndarray と numpy.matrix
> numpy.ndarray は多次元配列を扱うためのクラスです。
> numpy.matrix は２次元（行列）に特化したクラスです。
> ここまで説明してきたarrayオブジェクトは ndarrayのインスタンスオブジェクトで、
> matrixクラスでは演算子 `*` で行列の乗算を計算することができます。

線形代数学では行列の乗算のことを**行列の積(Matrix product)**といいます。
行列の積は次のようにしてもとまります。

[$ \left( \begin{array}{cc} a & b\\ \end{array} \right) \left(\begin{array}{cc} x\\ y\\ \end{array} \right) = ax + by]


[$ \left( \begin{array}{cc} a & b\\ c & d\\ \end{array} \right) \left(\begin{array}{cc} x\\ y\\ \end{array} \right) = \left( \begin{array}{cc} ax + by\\ cx + dy\\ \end{array} \right)]


[$ \left( \begin{array}{cc} a & b\\c & d\\ \end{array} \right) \left(\begin{array}{cc} x & y\\ z & t\\ \end{array} \right) = \left( \begin{array}{cc} ax + bz & ay + bt\\ cx + dz & cy + dt\\ \end{array} \right)]

 `m` 行 `n` 列の配列 `A` を、[$ A (m \times n)] と表記するとします。
まず、配列の乗算は A の列とBの行が同じサイズでないと計算できません。

[$ A (m \times n) \times B(n \times p) = C(m \times p)]

計算結果の配列 `C` は、配列 `A` の行サイズと配列 `B` の列サイズで構成された形状になります。

例えば、次の配列の乗算（行列の積）を求めてみます。

[$ \left( \begin{array}{cc} 1 & 2\\3 & 4\\ \end{array} \right) \left(\begin{array}{cc} 5 & 6\\ 7 & 8\\ \end{array} \right) = \left( \begin{array}{cc} 1 \times 5 + 2 \times 7 & 1 \ \times 6 + 2 \times 8\\ 3 \times 5 + 4 \times 7 & 3 \times 6 + 4 \times 8\\ \end{array} \right) = \left( \begin{array}{cc} 19 & 22\\43 & 50\\ \end{array} \right)]

次の例は、これを  `dot()` を使って計算したものです。
IPython
```
 In [2]: # %load numpy_dot1.py 
    ...: import numpy as np 
    ...:  
    ...: a = np.array([[1,2],[3,4]]) 
    ...: b = np.array([[5,6],[7,8]]) 
    ...:  
    ...: c = a.dot(b) 
    ...: d = np.dot(a, b) 
    ...:                                                                           
 
 In [3]: a                                                                 Out[3]: 
 array([[1, 2],
        [3, 4]])
 
 In [4]: b                                                                Out[4]: 
 array([[5, 6],
        [7, 8]])
 
 In [5]: c                                                                 Out[5]: 
 array([[19, 22],
        [43, 50]])
 
 In [6]: d                                                                 Out[6]: 
 array([[19, 22],
        [43, 50]])
 
 In [7]: a @ b                                                             Out[7]: 
 array([[19, 22],
        [43, 50]])
```

演算子 `@` を使っても行列の積を求めることができます。

### 転置行列(transposed matrix)
転置行列は、もとの行列の行と列を入れ替えたもので、 `array` オブジェクトの `.T` アトリビュートを参照すると得られます。一次元配列の場合は、そのまま同じ値を返します。

IPython
```
 In [2]: # %load numpy_transpose.py 
    ...: import numpy as np 
    ...:  
    ...: x = np.array([[1,2], [3,4]]) 
    ...: y = np.array([1,2,3]) 
    ...:  
    ...: x_t = x.T 
    ...: y_t = y.T 
    ...:                                                                           
 
 In [3]: x                                                                 Out[3]: 
 array([[1, 2],
        [3, 4]])
 
 In [4]: x_t                                                               Out[4]: 
 array([[1, 3],
        [2, 4]])
 
 In [5]: y                                                                 Out[5]: array([1, 2, 3])
 
 In [6]: y_t                                                               Out[6]: array([1, 2, 3])
```


### 要素の合計を求める
 `sum()` は配列の要素の合計を求めることができます。 `axis=0` で列、 `axis=1` で行の要素の合計を返します。
IPython
```
 In [2]: # %load numpy_sum.py 
    ...: import numpy as np 
    ...:  
    ...: x = np.array([[1,2],[3,4]]) 
    ...: a = np.sum(x) 
    ...: b = np.sum(x, axis=0) 
    ...: c = np.sum(x, axis=1) 
    ...:                                                                           
 
 In [3]: x                                                                 Out[3]: 
 array([[1, 2],
        [3, 4]])
 
 In [4]: a                                                                 Out[4]: 10
 
 In [5]: b                                                                 Out[5]: array([4, 6])
 
 In [6]: c                                                                 Out[6]: array([3, 7])
```

### ブロードキャスト
ブロードキャストは、行列計算をするときにさまざまな形状の配列を操作できるようにする、とても便利なしくみです。

例えば、行列の各行に定数ベクトルを加算したいときは、次のように書けます。
 IPython
```
 In [2]: # %load numpy_broadcasting1.py 
    ...: import numpy as np 
    ...:  
    ...: x = np.array([[1,2,3], [4,5,6], [7,8,9], [10, 11, 12]]) 
    ...: y = np.empty_like(x) 
    ...: v1 = np.array([1, 2, 3]) 
    ...:  
    ...: for i in range(4): 
    ...:     y[i, :] = x[i, :] + v1 
    ...:  
    ...: print(y) 
    ...:                                                                           
 [[ 2  4  6]
  [ 5  7  9]
  [ 8 10 12]
  [11 13 15]]
```

ただし、この方法では配列サイズが大きくなればなるほど効率が悪くなってしまいます。
 `tile()` は引数で与えた配列を、指定した数だけタイル状に積み重ねた `array` オブジェクトを生成して返します。そこで、 `tile()` を使って**定数ベクトルを配列サイズと同じ大きさ**にすれば、 `for` ループを使わなくても簡単に計算することができるようになります。

IPython
```
 In [2]: # %load numpy_broadcasting2.py 
    ...: import numpy as np 
    ...:  
    ...: x = np.array([[1,2,3], [4,5,6], [7,8,9], [10, 11, 12]]) 
    ...: y = np.empty_like(x) 
    ...: v1 = np.array([1, 2, 3]) 
    ...: v2 = np.tile(v1, (4, 1)) 
    ...:  
    ...: y = x + v2 
    ...: print(y) 
    ...:                                                                           
 [[ 2  4  6]
  [ 5  7  9]
  [ 8 10 12]
  [11 13 15]]
 
 In [3]: v2                                                                Out[3]: 
 array([[1, 2, 3],
        [1, 2, 3],
        [1, 2, 3],
        [1, 2, 3]])
```

先の２つの例は形状が同じ配列どおしで演算を行なっている場合ですね。

こんどは、配列のそれぞれの要素に定数を加算する例をみてましょう。
 IPython
```
 In [2]: # %load numpy_broadcastin３.py 
    ...: import numpy as np 
    ...:  
    ...: x = np.array([[1,2,3], [4,5,6], [7,8,9]]) 
    ...: y = x + 1 
    ...:
    ...: print(y) 
    ...:                                                                           
 [[ 2  3  4]
  [ 5  6  7]
  [ 8  9 10]]
```

簡単な例ですが、もし配列サイズが異なる演算ができないとすれば、
先の例のように、同じサイズの配列を別に作成しなければならないはずです。
IPython
```
 In [2]: # %load numpy_broadcasting4.py 
    ...: import numpy as np 
    ...:  
    ...: x = np.array([[1,2,3], [4,5,6], [7,8,9]]) 
    ...: v = np.full((3,3),1) 
    ...:  
    ...: y = x + v 
    ...: print(y) 
    ...:                                                                           
 [[ 2  3  4]
  [ 5  6  7]
  [ 8  9 10]]
 
 In [3]: v                                                                 Out[3]: 
 array([[1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]])
```

こんなことをしなくても numpy は  `x + 1` という記述を許してくれます。
これを実現してくれる仕組みがブロードキャスティングです。

ブロードキャスティング、次のようなルールで動作しています。

- 配列のランクが同じでないとき
  - 形状の長さが同じになるまで、より低いランクの配列の形状に1を加えていきます。
- 2つの配列の次元のサイズが同じか、配列の1つがその次元でサイズ1であるとき
  - 次元で互換性があると判断します。

すべての次元で互換性がある場合、配列どおしで一括操作することができます。
ブロードキャスト後、それぞれの配列は2つの入力配列の形状の要素ごとの最大値に等しい形状を持つように動作します。つまり、1つの配列のサイズが1で、もう1つの配列のサイズが1より大きい次元であれば、最初の配列はその次元でコピーされたかのように動作します。

もすこしわかりやすく説明してみましょう。
Python の数値（整数や浮動小数点数）は**スカラー(Scalar)**とよばれる 0 次元配列として扱われます。1 次元配列にスカラーを加えるような場合、スカラーを仮想的に 伸長して1 次元配列として演算を行います。

[$ \left( \begin{array}{cc} a & b & c\\ \end{array} \right)  + 1  \equiv  \left( \begin{array}{cc} a & b & c\\ \end{array} \right) + \left( \begin{array}{cc} 1 & 1 & 1\\ \end{array} \right)]


同様に２次元配列に１次元配列を加えるような場合も、１次元配列を仮想的に２次元配列に伸長して演算を行います。


[$ \left( \begin{array}{cc} a & b\\ c & d\\ \end{array} \right) +  \left(\begin{array}{cc} x & y\\ \end{array} \right)   \equiv   \left( \begin{array}{cc} a & b\\ c & d \\ \end{array} \right) + \left( \begin{array}{cc} x & y\\ x & y \\ \end{array} \right)]

列ベクトルに１次元配列を加えるような場合は、それぞれを互いのサイズに伸長して演算を行います。

[$ \left( \begin{array}{cc} a \\ b \\ c\\ \end{array} \right)  + \left( \begin{array}{cc} x & y & z\\ \end{array} \right)  \equiv  \left( \begin{array}{cc} a & a & a\\b & b & b\\c & c & c\\ \end{array} \right) + \left( \begin{array}{cc} x & y & z\\x & y & z\\x & y & z\\ \end{array} \right)]

これはブロードキャスティングの概念的な説明で、実際にはメモリ上への値のコピーなどは行われていないため、高速に演算処理が行われます。

 IPython
```
 In [2]: # %load numpy_broadcasting5.py 
    ...: import numpy as np 
    ...:  
    ...: x = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]]) 
    ...: y = np.array([1, 1, 1]) 
    ...:  
    ...: a = x + y 
    ...: print(a) 
    ...:                                                                           
 [[11 21 31]
  [41 51 61]
  [71 81 91]]
 
 In [3]: x                                                                 Out[3]: 
 array([[10, 20, 30],
        [40, 50, 60],
        [70, 80, 90]])
 
 In [4]: y                                                                 Out[4]: array([1, 1, 1])
```

#### broadcacst_to()  
 `broadcast_to()` は与えた配列を、指定した形状（shape）にブロードキャストします。
 IPython
```
 In [2]: # %load numpy_broadcast_to.py 
    ...: import numpy as np 
    ...:  
    ...: x = np.array([0, 1, 2]) 
    ...: y = np.broadcast_to(x, (4, 3)) 
    ...:  
    ...: print(y) 
    ...:                                                                           
 [[0 1 2]
  [0 1 2]
  [0 1 2]
  [0 1 2]]
 
 In [3]: x                                                                 Out[3]: array([0, 1, 2])
```

 `tile()` と似ているように見えますが、 `tile()` は与えた配列を指定した個数並べています。これに対して、 `broadcast_to()` は与えた配列を、指定したshapeに伸長させます。
このため、shapeには制限があり、行数を変えずに列数を増やすか、列数を変えずに行数を増やすことしかできません。つまり、1行3列の配列を、3行5列にはブロードキャスティングできません。
 `ValueError` が発生します。

#### broadcast_arrays()
 `broadcast_arrays()` は複数の配列を受け取って、ブロードキャストのルールにしたがってそれぞれの形状を合わせます。
 IPython
```
 In [2]: # %load numpy_broadcast_arrays.py 
    ...: import numpy as np 
    ...: from pprint import pprint 
    ...:  
    ...: x = np.array([0, 1, 2]) 
    ...: y = np.array([[10], [20], [30]]) 
    ...: z = 1 
    ...:  
    ...: a = np.broadcast_arrays(x, y, z) 
    ...: pprint(a) 
    ...:                                                                           
 [array([[0, 1, 2],
        [0, 1, 2],
        [0, 1, 2]]),
  array([[10, 10, 10],
        [20, 20, 20],
        [30, 30, 30]]),
  array([[1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]])]
  In [3]: x                                                                 Out[3]: array([0, 1, 2])
  
  In [4]: y                                                                 Out[4]: 
  array([[10],
         [20],
         [30]])
        
```
ブロードキャスティングできない組み合わせの配列が与えられていると `ValueError` が発生します。

### 配列の連結と分割
 `NumPy` で、配列の連結や分割を行う関数が提供されています。

- 配列の連結
  -  `numpy.concatenate()` ：配列の連結
  -  `numpy.vstack()` ：縦方向に連結/行で連結
  -  `numpy.hstack()` ：横方向に連結/列で連結
- 配列の分割
  -  `numpy.split()` ：均等分割
  -  `numpy.array_split()` ：なるべく均等に分割
  -  `numpy.vsplit()` ：縦方向に分割/行で分割
  -  `numpy.hsplit()` ：横方向に分割/列で分割

numpy には他に多くの応用範囲に適用できるクラスや関数が提供されています。
独自で実装しなくても、コードを簡潔に記述でき、高速に計算ができますよ。

## 参考
- [numpy.org: NumPyオフィシャルサイト  ](https://numpy.org/)
- [Anaconda Python ](https://www.anaconda.com/distribution/)
- [Intel Distribution for Python ](https://software.intel.com/en-us/distribution-for-python)
- [行列のランクの意味（８通りの同値な定義）　](https://mathtrain.jp/matrixrank)
　[](https://python.atelierkobato.com/rank/)



