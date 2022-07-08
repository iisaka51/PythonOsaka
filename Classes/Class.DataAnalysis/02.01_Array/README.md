Python の arrayモジュールを使ってみよう
=================
Python の  `array` モジュールは、基本的な値 (文字、整数、浮動小数点数) の
#### 配列 (array)

 `array` はデータ型固定のシーケンスで、リストと同じように使えますが、要素にできるオブジェクト型には制限があり、初期化時に指定した型コードに該当するオブジェクト型しか保持できません。その制約のおかげでメモリ使用の無駄がすくなくなるわけです。

> array(typecode [, initializer]) -> array
>     typecode: 型コード
>     initializer: 初期化データ
>     array型オブジェクトを返します

型コードには初期化時に次の値を指定します。


| 型コード | Cの型 | Pythonの型 | 最小サイズ (Byte単位) |
|:--|:--|:--|:--|
| b | signed char | int | 1 |
| B | unsigned char | int | 1 |
| u | Py_UNICODE | Unicode文字(unicode型) | 2 |
| h | signed short | int | 2 |
| H | unsigned short | int | 2 |
| i(小文字アイ) | signed int  | int | 2 |
| I(大文字アイ) | unsigned int | int | 2 |
| l(小文字エル) | signed long | int | 4 |
| L | unsigned long | int | 4 |
| q | signed long long | int | 8 |
| Q | unsigned long long | int | 8 |
| f | float | float | 4 |
| d | double | float | 8 |

 IPython
```
 In [2]: # %load array_demo.py 
    ...: import array 
    ...:  
    ...: a = array.array('d', [1.0, 2.0, 3.14]) 
    ...:                                                                    
 In [3]: a                                                                 Out[3]: array('d', [1.0, 2.0, 3.14])
```

指定できる型コードからわかるように、 `array` 型や `list` 型のオブジェクトは要素にできません。つまり、 `array` 型は１次元の配列しか扱えないことになります。

###  ファイル入出力
 `array` 型オブジェクトはファイル入出力ができるメソッドをもっています。

-  `tofile()` ：指定したファイルに書き出す
-  `fromfile()` ：指定したファイルから読み込む

まず、例を見てみましょう。
 IPython
```
 In [2]: # %load array_fileio.py 
    ...: import array 
    ...: import binascii 
    ...: import tempfile 
    ...:  
    ...: data = array.array('i', range(5)) 
    ...: print(f'Original data:{data}') 
    ...:  
    ...: output = tempfile.NamedTemporaryFile() 
    ...: data.tofile(output.file) 
    ...: output.flush() 
    ...:  
    ...: input = open(output.name, 'rb') 
    ...: raw_data = input.read() 
    ...: print(f'Raw Data: {binascii.hexlify(raw_data)}') 
    ...:  
    ...: input.seek(0) 
    ...: read_data = array.array('i') 
    ...: read_data.fromfile(input, len(data)) 
    ...: print(f'Read Data: {read_data}') 
    ...:                                                                           
 Original data:array('i', [0, 1, 2, 3, 4])
 Raw Data: b'0000000001000000020000000300000004000000'
 Read Data: array('i', [0, 1, 2, 3, 4])
```

 `array` 型の `tofile()` と  `fromfile()` メソッドは、ファイルオブジェクトを与えて、
オブジェクトが保持しているデータを読み書きします。


参考:
- [Python公式ドキュメント array ](https://docs.python.org/ja/3/library/array.html)



