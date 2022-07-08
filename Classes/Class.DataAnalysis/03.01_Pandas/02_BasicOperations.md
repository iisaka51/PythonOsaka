Pandasの基本操作
=================

### Pandas のオブジェクト型
Pandas では次の２つのオブジェクト型が提供されます。

-  `Series` ：一次元の配列データ。
-  `DataFrame` ：２次元配列：行と列で構成される表形式データ

> Pandas には ３次元データを扱うPanel型というものもありましたが、
> Version 0.25.0 で削除されています。

### Series型の基本操作
 `Series` 型は２つの作成方法があります。

```
 import pandas as pd
 
 s1 = pd.Series(range(10))
 print(s1.head())
 
 s2 = pd.Series([1, 2, 3], index=['One', 'Two', 'Three'])
 print(s2.head())
 
 s3 = pd.Series({'One':1, 'Two':2, 'Three':3})
 print(s3.head())
 
 s3 = s3.append(pd.Series({'Four':4}))
 
 print(s3.head())
```

 bash
```
 $ python  pandas_series_demo.py 
 0    0
 1    1
 2    2
 3    3
 4    4
 dtype: int64
 One      1
 Two      2
 Three    3
 dtype: int64
 One      1
 Two      2
 Three    3
 dtype: int64
 One      1
 Two      2
 Three    3
 Four     4
 dtype: int64
```

 `s1` は `Range` オブジェクトをそのまま `Series` 型にしています。このときはインデックスはゼロはじまりの数値が自動的に割り振られます。同様に、 `list` 型から `Series` 型を生成することもできます。
 `s2` はインデックスを明示的に指定したいときは、 `index=[]` のようにインデックスをリストで与えます。
 `s3` は辞書型オブジェクトから  `Series` 型を生成させています。このとき、インデックスは辞書のキーが割り振られます。

 `Series` 型オブジェクトの連結には  `append()` メソッドを使います。
 IPython
```
 In [2]: # %load pandas_series_append.py 
    ...: import pandas as pd 
    ...:  
    ...: s1 = pd.Series(range(5)) 
    ...: s2 = pd.Series([1, 2, 3], index=['One', 'Two', 'Three']) 
    ...: s3 = pd.Series({'One':1, 'Two':2, 'Three':3}) 
    ...:  
    ...: print(s3) 
    ...: s3 = s3.append(pd.Series({'Four':4})) 
    ...: print(s3) 
    ...:                                                                           
 One      1
 Two      2
 Three    3
 dtype: int64
 One      1
 Two      2
 Three    3
 Four     4
 dtype: int64
                                                                        
 In [3]: s1.index                                                          Out[3]: RangeIndex(start=0, stop=5, step=1)
 
 In [4]: s1.values                                                         Out[4]: array([0, 1, 2, 3, 4])
 
 In [5]: s2.index                                                          Out[5]: Index(['One', 'Two', 'Three'], dtype='object')
 
 In [6]: s2.values                                                         Out[6]: array([1, 2, 3])
 
 In [7]: s3.index                                                          Out[7]: Index(['One', 'Two', 'Three', 'Four'], dtype='object')
 
 In [8]: s3.values                                                         Out[8]: array([1, 2, 3, 4])
```

### Series型の要素を抽出
要素の抽出するためには、番号を指定するarray型と、インデックスの文字列を指定する辞書型の２つの方法があります。


```
 In [9]: s3[2]                                                             Out[9]: 3
 
 In [10]: s3['Three']                                                      Out[10]: 3
```

また、条件を指定することもできます。

```
 In [11]: s3[s3 > 2]                                                       Out[11]: 
 Three    3
 Four     4
 dtype: int64
```

### インデックスの有無を確認
キーが `Series` 型オブジェクトにあるかを確認するためには  `in` を使います。

```
 In [12]: 'Three' in s3                                                            
 Out[12]: True
 
 In [13]: 'Five' in s3                                                             
 Out[13]: False
```

### Series型オブジェクトの要素にNULLがあるか調べる
 `Series` 型オブジェクトの要素にNULLがあるかを調べるには、 `isnull()` と  `notnull()` を使います。

```
 In [17]: pd.isnull(s3)                                                    Out[17]: 
 One      False
 Two      False
 Three    False
 Four     False
 dtype: bool
 
 In [18]: pd.notnull(s3)                                                   Out[18]: 
 One      True
 Two      True
 Three    True
 Four     True
 dtype: bool
```

### Series型オブジェクトの演算
 `Series` 型オブジェクトどうしを演算すると、同じインデックスがあればそれを演算した結果を `Series` 型オブジェクトとして返します。
どちらかに無いインデックスがあるときは `NaN` がセットされます。


```
 In [19]: s1 = pd.Series({'Beer':1000, 'Wine':800, 'Sake':750}) 
     ...: s2 = pd.Series({'Beer':1200, 'Wine':2000}) 
     
 In [20]: s1                                                               Out[20]: 
 Beer    1000
 Wine     800
 Sake     750
 dtype: int64
 
 In [21]: s2                                                               Out[21]: 
 Beer    1200
 Wine    2000
 dtype: int64
 
 In [22]: s1 + s2                                                          Out[22]: 
 Beer    2200.0
 Sake       NaN
 Wine    2800.0
 dtype: float64
 
 In [23]: s2 - s1                                                          Out[23]: 
 Beer     200.0
 Sake       NaN
 Wine    1200.0
 dtype: float64
 
 In [24]: s1 * s2                                                          Out[24]: 
 Beer    1200000.0
 Sake          NaN
 Wine    1600000.0
 dtype: float64
```


### 名前の設定
 `Series` 型オブジェクトには名前をつけることができます。


```
 In [25]: s1.name = 'Drink Prices'                                         In [26]: s1.index.name = 'Item'                                           In [27]: s1                                                               Out[27]: 
 Item
 Beer    1000
 Wine     800
 Sake     750
 Name: Drink Prices, dtype: int64
```

### DataFrame型の基本操作
 `DataFrame` 型は行と列から構成される２次元のデータとなります。

![](https://gyazo.com/3b4705a659d8842dcd5f9e506568d8fb.png)
出典：[Python Pandas Tutorial: A Complete Introduction for Beginners ](https://www.learndatasci.com/tutorials/python-pandas-tutorial-complete-introduction-for-beginners/)

 `Series` 型と同じように `list` 型から `DataFrame` オブジェクトを生成することができます。

 pandas_dataframe_sample1.py
```
 import pandas as pd
 data = [
     ['01', '02', '03', '04', '05'],
     ['11', '12', '13', '14', '15'],
     ['21', '22', '23', '24', '25'],
 ]
 
 df = pd.DataFrame(data)
```


 IPython
```
 In [3]: # %load pandas_dataframe_sample1.py 
    ...: import pandas as pd 
    ...: data = [ 
    ...:     ['01', '02', '03', '04', '05'], 
    ...:     ['11', '12', '13', '14', '15'], 
    ...:     ['21', '22', '23', '24', '25'], 
    ...: ] 
    ...:  
    ...: df = pd.DataFrame(data) 
    ...:                                                                           
 In [4]: data                                                              Out[4]: 
 [['01', '02', '03', '04', '05'],
  ['11', '12', '13', '14', '15'],
  ['21', '22', '23', '24', '25']]
 
 In [5]: df                                                                Out[5]: 
     0   1   2   3   4
 0  01  02  03  04  05
 1  11  12  13  14  15
 2  21  22  23  24  25
```

 `list` 型から `DataFrame` 型オブジェクトを生成すると、行ごとに読んでいくように処理されます。

 pandas_dataframe_sample2.py
```
 import pandas as pd
 history_data = [
     ['2015-01-05', '2015-01-06', '2015-01-07', '2015-01-08'],
     ['7565.0', '7322.0', '7256.0', '7500.0'],
     [ '7507.0', '7300.0', '7407.0', '7554.0'],
 ]
 
 history_df = pd.DataFrame(history_data)
```


 IPython
```
  In [2]: # %load pandas_dataframe_sample2.py 
    ...: import pandas as pd 
    ...: history_data = [ 
    ...:     ['2015-01-05', '2015-01-06', '2015-01-07', '2015-01-08'], 
    ...:     ['7565.0', '7322.0', '7256.0', '7500.0'], 
    ...:     [ '7507.0', '7300.0', '7407.0', '7554.0'], 
    ...: ] 
    ...:  
    ...: history_df = pd.DataFrame(history_data) 
    ...:                                                                           
 In [3]: history_df                                                        Out[3]: 
             0           1           2           3
 0  2015-01-05  2015-01-06  2015-01-07  2015-01-08
 1      7565.0      7322.0      7256.0      7500.0
 2      7507.0      7300.0      7407.0      7554.0
```

 `Series` 型と同様に `dict` 型データから `DataFrame` 型を生成することができます。
この場合は、列ごとに読んでいくように処理されます。

 pandas_dataframe_sample3.py
```
 import pandas as pd
 history_data = {
     'Date':['2015-01-05', '2015-01-06', '2015-01-07', '2015-01-08'],
     'Open':['7565.0', '7322.0', '7256.0', '7500.0'],
     'Close':[ '7507.0', '7300.0', '7407.0', '7554.0'],
 }
 
 history_df = pd.DataFrame(history_data)
```


 IPython
```
 In [2]: # %load pandas_dataframe_sample3.py 
    ...: import pandas as pd 
    ...: history_data = { 
    ...:     'Date':['2015-01-05', '2015-01-06', '2015-01-07', '2015-01-08'], 
    ...:     'Open':['7565.0', '7322.0', '7256.0', '7500.0'], 
    ...:     'Close':[ '7507.0', '7300.0', '7407.0', '7554.0'], 
    ...: } 
    ...:  
    ...: history_df = pd.DataFrame(history_data) 
    ...:                                                                           
 
 In [3]: history_df                                                                
 Out[3]: 
          Date    Open   Close
 0  2015-01-05  7565.0  7507.0
 1  2015-01-06  7322.0  7300.0
 2  2015-01-07  7256.0  7407.0
 3  2015-01-08  7500.0  7554.0
```

 `DataFrame` オブジェクトの  `index` と  `columns` にリストで与えるとインデックス名やカラム名を変更することができます。
 IPython
```
 In [3]: df                                                                Out[3]: 
     0   1   2   3   4
 0  01  02  03  04  05
 1  11  12  13  14  15
 2  21  22  23  24  25
 
 In [4]: df.columns=['A','B', 'C', 'D', 'E']                               In [5]: df.index=['000', '001', '002']                                    In [6]: df                                                                Out[6]: 
       A   B   C   D   E
 000  01  02  03  04  05
 001  11  12  13  14  15
 002  21  22  23  24  25
```

### DataFrameオブジェクトの追加
 `DataFrame` オブジェクトの `append()` を使うことで、**行** を追加することができます。


```
 In [3]: history_df1                                                       Out[3]: 
          Date    Open   Close
 0  2015-01-05  7565.0  7507.0
 1  2015-01-06  7322.0  7300.0
 2  2015-01-07  7256.0  7407.0
 3  2015-01-08  7500.0  7554.0
 
 In [4]: history_df2                                                       Out[4]: 
          Date    Open   Close
 0  2015-01-09  7630.0  7609.0
 1  2015-01-10  7440.0  7519.0
 
 In [5]: df = history_df1.append(history_df2)                              In [6]: df                                                                Out[6]: 
          Date    Open   Close
 0  2015-01-05  7565.0  7507.0
 1  2015-01-06  7322.0  7300.0
 2  2015-01-07  7256.0  7407.0
 3  2015-01-08  7500.0  7554.0
 0  2015-01-09  7630.0  7609.0
 1  2015-01-10  7440.0  7519.0
 
 In [7]: history_df1                                                       Out[7]: 
          Date    Open   Close
 0  2015-01-05  7565.0  7507.0
 1  2015-01-06  7322.0  7300.0
 2  2015-01-07  7256.0  7407.0
 3  2015-01-08  7500.0  7554.0
```

#### 列
該当するカラム名が `DataFrame` オブジェクトにあれば置き換えられます。

 IPython
```
 In [2]: # %load pandas_dataframe_append2.py 
    ...: import pandas as pd 
    ...: history_data = { 
    ...:     'Date':['2015-01-05', '2015-01-06', '2015-01-07', '2015-01-08'], 
    ...:     'Open':['7565.0', '7322.0', '7256.0', '7500.0'], 
    ...:     'Close':[ '7507.0', '7300.0', '7407.0', '7554.0'], 
    ...: } 
    ...: adjClose_data = [ 
    ...:     '6402.83447265625', 
    ...:     '6226.2802734375', 
    ...:     '6317.54296875', 
    ...:     '6442.92138671875', 
    ...: ] 
    ...:  
    ...: history_df = pd.DataFrame(history_data) 
    ...: history_df['AdjClose'] = adjClose_data 
    ...:                                                                   
 In [3]: history_df                                                        Out[3]: 
          Date    Open   Close          AdjClose
 0  2015-01-05  7565.0  7507.0  6402.83447265625
 1  2015-01-06  7322.0  7300.0   6226.2802734375
 2  2015-01-07  7256.0  7407.0     6317.54296875
 3  2015-01-08  7500.0  7554.0  6442.92138671875
 
 In [4]: history_df['AdjClose'] = adjClose_data                            In [5]: history_df                                                        Out[5]: 
          Date    Open   Close          AdjClose
 0  2015-01-05  7565.0  7507.0  6402.83447265625
 1  2015-01-06  7322.0  7300.0   6226.2802734375
 2  2015-01-07  7256.0  7407.0     6317.54296875
 3  2015-01-08  7500.0  7554.0  6442.92138671875
 
 In [6]: adjClose_data[0]=6402                                             In [7]: adjClose_data                                                     Out[7]: [6402, '6226.2802734375', '6317.54296875', '6442.92138671875']
 
 In [8]: history_df['AdjClose'] = adjClose_data                            In [9]: history_df                                                        Out[9]: 
          Date    Open   Close          AdjClose
 0  2015-01-05  7565.0  7507.0              6402
 1  2015-01-06  7322.0  7300.0   6226.2802734375
 2  2015-01-07  7256.0  7407.0     6317.54296875
 3  2015-01-08  7500.0  7554.0  6442.92138671875
```

 `DataFrame` オブジェクトの  `index` と `columns` を参照するとインデクス名とカラム名を知ることができます。
 IPython
```
 In [3]: history_df                                                        Out[3]: 
          Date    Open   Close
 0  2015-01-05  7565.0  7507.0
 1  2015-01-06  7322.0  7300.0
 2  2015-01-07  7256.0  7407.0
 3  2015-01-08  7500.0  7554.0
 
 In [4]: history_df.index                                                  Out[4]: RangeIndex(start=0, stop=4, step=1)
 
 In [5]: history_df.columns                                                Out[5]: Index(['Date', 'Open', 'Close'], dtype='object')
 
```

### DataFrameのデータ内容を参照する
 `DataFrame` オブジェクト内容を知るためには  `values` を参照します。
このとき `DataFrame` オブジェクトを生成した方法により少し結果が異なります。

 IPython
```
 In [6]: history_data.values                                               Out[6]: <function dict.values>
 
 In [7]: history_data.values()                                             Out[7]: dict_values([['2015-01-05', '2015-01-06', '2015-01-07', '2015-01-08'], ['7565.0', '7322.0', '7256.0', '7500.0'], ['7507.0', '7300.0', '7407.0', '7554.0']])
 
```
 `dict` 型オブジェクトから `DataFrame` オブジェクトを生成したときは、
 `DataFrame.values` は  `dict.values` となり、保持しているデータを参照するためには、
メソッド関数としてアクセスする必要が’あります。
 IPython
```
 In [9]: # %load pandas_dataframe_sample1.py 
    ...: import pandas as pd 
    ...: data = [ 
    ...:     ['01', '02', '03', '04', '05'], 
    ...:     ['11', '12', '13', '14', '15'], 
    ...:     ['21', '22', '23', '24', '25'], 
    ...: ] 
    ...:  
    ...: df = pd.DataFrame(data) 
    ...:                                                                           
 In [10]: df                                                               Out[10]: 
     0   1   2   3   4
 0  01  02  03  04  05
 1  11  12  13  14  15
 2  21  22  23  24  25
 
 In [11]: df.index                                                         Out[11]: RangeIndex(start=0, stop=3, step=1)
 
 In [12]: df.columns                                                       Out[12]: RangeIndex(start=0, stop=5, step=1)
 
 In [13]: df.values                                                        Out[13]: 
 array([['01', '02', '03', '04', '05'],
        ['11', '12', '13', '14', '15'],
        ['21', '22', '23', '24', '25']], dtype=object)
```

 `list` 型オブジェクトから `DataFrame` オブジェクトを生成したときは、
 `DataFrame.values` でデータの内容を知ることができます。

 `head()` と  `tail()` は指定した行数を表示します。
-  `head(N)` ： 先頭からN行を表示。デフォルトは５
-  `tail(N)` ：最後のN行を表示。デフォルトは５

### データ抽出
カラム名を指定するとそのカラムのデータを抽出して `DataFrame` オブジェクトとして返します。そのとき、指定方法には、ピリオド( `.` )に続けてカラム名を指定する方法と、辞書型のキーのようにカラム名を指定する２つの方法があります。
 IPython
```
 In [12]: history_df                                                       Out[12]: 
          Date    Open   Close
 0  2015-01-05  7565.0  7507.0
 1  2015-01-06  7322.0  7300.0
 2  2015-01-07  7256.0  7407.0
 3  2015-01-08  7500.0  7554.0
 
 In [13]: d1 = history_df.Open                                             In [14]: d2 = history_df['Open']                                          In [15]: df1                                                              Out[15]: 
 0    7565.0
 1    7322.0
 2    7256.0
 3    7500.0
 Name: Open, dtype: object
 
 In [16]: df2                                                              Out[16]: 
 0    7565.0
 1    7322.0
 2    7256.0
 3    7500.0
 Name: Open, dtype: object
```

複数のカラムを抽出したいときは、リストで渡します。

```
 In [26]: history_df                                                       Out[26]: 
          Date    Open   Close
 0  2015-01-05  7565.0  7507.0
 1  2015-01-06  7322.0  7300.0
 2  2015-01-07  7256.0  7407.0
 3  2015-01-08  7500.0  7554.0
 
 In [27]: df = history_df[['Open', 'Close']]                               In [28]: df                                                               Out[28]: 
      Open   Close
 0  7565.0  7507.0
 1  7322.0  7300.0
 2  7256.0  7407.0
 3  7500.0  7554.0
```

行を抽出したいときは、 `iloc()` メソッドを呼び出します。
Ipython
```
 In [2]: # %load pandas_dataframe_sample1.py  
    ...: import pandas as pd 
    ...: data = [ 
    ...:     ['01', '02', '03', '04', '05'], 
    ...:     ['11', '12', '13', '14', '15'], 
    ...:     ['21', '22', '23', '24', '25'], 
    ...: ] 
    ...:  
    ...: df = pd.DataFrame(data) 
    ...:                                                                   
 In [3]: df.iloc[1]                                                        Out[3]: 
 0    11
 1    12
 2    13
 3    14
 4    15
 Name: 1, dtype: object
 
 In [4]: df.iloc[1][2]                                                     Out[4]: '13'
```

### shape と ndim
 `NumPy` の `ndarray` 型と同じく、Pandasの `Series` 型と `DataFrame` 型オブジェクトでも
 `shape` アトリビュートを参照することでデータの形状を知ることができます。
また、 `ndim` アトリビュートを参照することでデータの次元数を知ることができます。
 `Series` 型のオブジェクトでは１， `DataFrame` 型オブジェクトでは２となります。


### describe() で統計情報を表示 
 `Series` オブジェクト、 `DataFrame` オブジェクトはともに  `describe()` メソッドを持っていて、これを呼び出すとデータの統計情報を表示してくれます。
保持しているデータにより、表示される内容が異なります。

数値データを保持しているときは、平均値（ `mean` )や、最大( `max` )、最小( `min` ) などを表示します。
 IPython
```
 In [2]: s = pd.Series([1, 2, 3, 4, 5])                                    In [3]: s                                                                 Out[3]: 
 0    1
 1    2
 2    3
 3    4
 4    5
 dtype: int64
 
 In [4]: s.describe()                                                      Out[4]: 
 count    5.000000
 mean     3.000000
 std      1.581139
 min      1.000000
 25%      2.000000
 50%      3.000000
 75%      4.000000
 max      5.000000
 dtype: float64
```

文字列データを保持しているときは、データの総数( `count` ) やユニーク数( `uniq` )、重複回数( `freq` )などの統計情報を表示します。
 Ipython
```
 In [5]: s = pd.Series(['A', 'B', 'C', 'D', 'E'])                          In [6]: s                                                                 Out[6]: 
 0    A
 1    B
 2    C
 3    D
 4    E
 dtype: object
 
 In [7]: s.describe()                                                      Out[7]: 
 count     5
 unique    5
 top       D
 freq      1
 dtype: object
```

時系列データや日時情報を保持しているときは、文字列データの統計情報に加えて、
もっとも古い日時情報( `first` ) ともっとも新しい日時情報( `last` ) を表示します。
 IPython
```
 In [16]: s = pd.Series([ 
     ...: datetime(2020,1,1), 
     ...: datetime(2020,1,2), 
     ...: datetime(2020,1,3), 
     ...: datetime(2020,1,4)])                                                     
 In [17]: s                                                                Out[17]: 
 0   2020-01-01
 1   2020-01-02
 2   2020-01-03
 3   2020-01-04
 dtype: datetime64[ns]
 
 In [18]: s.describe()                                                     Out[18]: 
 count                       4
 unique                      4
 top       2020-01-03 00:00:00
 freq                        1
 first     2020-01-01 00:00:00
 last      2020-01-04 00:00:00
 dtype: object
```

 `DataFrame` オブジェクトの場合は、 `describe()` メソッドはデフォルトでは数値データについて統計情報を表示します。
 `describe(include='all')` として呼び出すと、全てのデータについて統計情報を表示します。

 pandas_dataframe_sample5.py
```
 from datetime import datetime
 import pandas as pd
 history_data = {
     'Date':[
         datetime(2015,1,5),
         datetime(2015,1,6),
         datetime(2015,1,7),
         datetime(2015,1,8)
         ],
     'Open':[7565.0, 7322.0, 7256.0, 7500.0],
     'Close':[ 7507.0, 7300.0, 7407.0, 7554.0],
 }
     
 history_df = pd.DataFrame(history_data)
     
```


 IPython
```
 In [2]: # %load pandas_dataframe_sample5.py 
    ...: from datetime import datetime 
    ...: import pandas as pd 
    ...: history_data = { 
    ...:     'Date':[ 
    ...:         datetime(2015,1,5), 
    ...:         datetime(2015,1,6), 
    ...:         datetime(2015,1,7), 
    ...:         datetime(2015,1,8) 
    ...:         ], 
    ...:     'Open':[7565.0, 7322.0, 7256.0, 7500.0], 
    ...:     'Close':[ 7507.0, 7300.0, 7407.0, 7554.0], 
    ...: } 
    ...:  
    ...: history_df = pd.DataFrame(history_data) 
    ...:                                                                           
 In [3]: history_df                                                        Out[3]: 
         Date    Open   Close
 0 2015-01-05  7565.0  7507.0
 1 2015-01-06  7322.0  7300.0
 2 2015-01-07  7256.0  7407.0
 3 2015-01-08  7500.0  7554.0
 
 In [4]: history_df.describe()                                             Out[4]: 
               Open        Close
 count     4.000000     4.000000
 mean   7410.750000  7442.000000
 std     145.582451   112.780022
 min    7256.000000  7300.000000
 25%    7305.500000  7380.250000
 50%    7411.000000  7457.000000
 75%    7516.250000  7518.750000
 max    7565.000000  7554.000000
 
 In [5]: history_df.describe(include='all')                                Out[5]: 
                        Date         Open        Close
 count                     4     4.000000     4.000000
 unique                    4          NaN          NaN
 top     2015-01-07 00:00:00          NaN          NaN
 freq                      1          NaN          NaN
 first   2015-01-05 00:00:00          NaN          NaN
 last    2015-01-08 00:00:00          NaN          NaN
 mean                    NaN  7410.750000  7442.000000
 std                     NaN   145.582451   112.780022
 min                     NaN  7256.000000  7300.000000
 25%                     NaN  7305.500000  7380.250000
 50%                     NaN  7411.000000  7457.000000
 75%                     NaN  7516.250000  7518.750000
 max                     NaN  7565.000000  7554.000000
 
```
 `include=` にはオブジェクト型のリストを与えることができます。
また、 `exclude=` を指定すると、そのデータ型は対象外となります。

 IPython
```
 In [22]: history_df.Date                                                  Out[22]: 
 0   2015-01-05
 1   2015-01-06
 2   2015-01-07
 3   2015-01-08
 Name: Date, dtype: datetime64[ns]
 
 In [23]: history_df.describe(include=['datetime64'])                      Out[23]: 
                        Date
 count                     4
 unique                    4
 top     2015-01-07 00:00:00
 freq                      1
 first   2015-01-05 00:00:00
 last    2015-01-08 00:00:00
 
 In [24]: history_df.Open                                                  Out[24]: 
 0    7565.0
 1    7322.0
 2    7256.0
 3    7500.0
 Name: Open, dtype: float64
 
 In [25]: history_df.describe(include=['float64'])                         Out[25]: 
               Open        Close
 count     4.000000     4.000000
 mean   7410.750000  7442.000000
 std     145.582451   112.780022
 min    7256.000000  7300.000000
 25%    7305.500000  7380.250000
 50%    7411.000000  7457.000000
 75%    7516.250000  7518.750000
 max    7565.000000  7554.000000
 
 In [26]: history_df.describe(exclude=['datetime64'])                      Out[26]: 
               Open        Close
 count     4.000000     4.000000
 mean   7410.750000  7442.000000
 std     145.582451   112.780022
 min    7256.000000  7300.000000
 25%    7305.500000  7380.250000
 50%    7411.000000  7457.000000
 75%    7516.250000  7518.750000
 max    7565.000000  7554.000000
 
```

### DataFrameをソート
 Ipython
```
 In [2]: # %load pandas_dataframe_sort.py 
    ...: import pandas as pd 
    ...:  
    ...: data = {'Brand': ['A','B','C','D'], 
    ...:         'Price': [1000,1200,800,1900], 
    ...:         'Year': [2020,2017,2018,2016] 
    ...:         } 
    ...:  
    ...: df = pd.DataFrame(data, columns= ['Brand', 'Price','Year']) 
    ...: print (df) 
    ...:                                                                           
   Brand  Price  Year
 0     A   1000  2020
 1     B   1200  2017
 2     C    800  2018
 3     D   1900  2016
```

#### カラム名を指定してソード
 `sort_values()` にデータをソートするカラム名を指定します。
 `ascending=True` とすると昇順にソートし、 `inplace=True` でデータを置き換えます。
 IPytho 
```
 In [11]: df.sort_values("Brand", inplace=True, ascending=False)            In [12]: df                                                                Out[12]: 
   Brand  Price  Year
 3     D   1900  2016
 2     C    800  2018
 1     B   1200  2017
 0     A   1000  2020
```

 `inplace=False` とするとソートされた `DataFrame` オブジェクトが返されます。
 IPython
```
 In [14]: df.sort_values("Brand", inplace=False, ascending=True)            Out[14]: 
   Brand  Price  Year
 0     A   1000  2020
 1     B   1200  2017
 2     C    800  2018
 3     D   1900  2016
 
 In [15]: df                                                                Out[15]: 
   Brand  Price  Year
 3     D   1900  2016
 2     C    800  2018
 1     B   1200  2017
 0     A   1000  2020
 
```

#### インデックスでソード
 `sort_index()` を使うとカラム名やインデックスでソートします。
 `ascending=True` とすると昇順にソートし、 `inplace=True` でデータを置き換えます。
 IPython
```
 In [24]: df.sort_index(axis=0,ascending=False,inplace=True)                In [25]: df                                                                Out[25]: 
   Brand  Price  Year
 3     D   1900  2016
 2     C    800  2018
 1     B   1200  2017
 0     A   1000  2020
 
 In [26]: df.sort_index(axis=0,ascending=True)                              Out[26]: 
   Brand  Price  Year
 0     A   1000  2020
 1     B   1200  2017
 2     C    800  2018
 3     D   1900  2016
 
```

 `axis=0` でインデックス、 `axis=1` でカラムでソートします。
 IPython
```
 In [27]: df.sort_index(axis=1,ascending=True)                              Out[27]: 
   Brand  Price  Year
 3     D   1900  2016
 2     C    800  2018
 1     B   1200  2017
 0     A   1000  2020
 
 In [28]: df.sort_index(axis=1,ascending=False)                             Out[28]: 
    Year  Price Brand
 3  2016   1900     D
 2  2018    800     C
 1  2017   1200     B
 0  2020   1000     A
```

### グルーピング
 `groupby()` にグルーピングを行うカラム名を指定します。
そのグループ化された単位で統計情報などの計算や処理を行うことができます。
 IPython
```
 In [2]: # %load pandas_dataframe_groupby.py 
    ...: import numpy as np 
    ...: import pandas as pd 
    ...:  
    ...: data = {'Brand': ['A','B','A','C','B','D'], 
    ...:         'Price': [1000,1200,1000,800,1200,1900], 
    ...:         'Year': [2020,2017,2020,2018,2017,2016] 
    ...:         } 
    ...:  
    ...: df = pd.DataFrame(data, columns= ['Brand', 'Price','Year']) 
    ...: print (df) 
    ...:                                                                           
   Brand  Price  Year
 0     A   1000  2020
 1     B   1200  2017
 2     A   1000  2020
 3     C    800  2018
 4     B   1200  2017
 5     D   1900  2016
 
 In [3]: df2 = df.groupby("Brand")   
 In [4]: df2.aggregate(np.mean)["Price"]                                   Out[4]: 
 Brand
 A    1000
 B    1200
 C     800
 D    1900
 Name: Price, dtype: int64
 
 In [5]: df2.aggregate(np.sum)["Price"]                                     Out[5]: 
 Brand
 A    2000
 B    2400
 C     800
 D    1900
 Name: Price, dtype: int64
```

### データフレームに関数を適用する
 `apply()` を使うと、データフレームを関数で処理させることができます。
 IPython
```
 In [27]: df2 = df.groupby("Price")                                         In [28]: df2.apply(np.mean)                                                Out[28]: 
         Price    Year
 Price                
 800     800.0  2018.0
 1000   1000.0  2020.0
 1200   1200.0  2017.0
 1900   1900.0  2016.0
 
 In [29]: df2.apply(lambda x: np.mean(x))                                   Out[29]: 
         Price    Year
 Price                
 800     800.0  2018.0
 1000   1000.0  2020.0
 1200   1200.0  2017.0
 1900   1900.0  2016.0
```


### DatetimeIndex
Pandas では時系列データも扱うことができます。
そのときに便利な関数が  `date_range()` です。
 Ipython
```
 In [2]: # %load pandas_index.py 
    ...: import pandas as pd 
    ...:  
    ...: dr_1 = pd.date_range(start='2020/1/1', end='2020/1/08') 
    ...: dr_2 = pd.date_range(start='1/1/2020', end='1/08/2020') 
    ...:  
    ...: print(dr_1) 
    ...: print(dr_2) 
    ...:                                                                           
 DatetimeIndex(['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04',
                '2020-01-05', '2020-01-06', '2020-01-07', '2020-01-08'],
               dtype='datetime64[ns]', freq='D')
 DatetimeIndex(['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04',
                '2020-01-05', '2020-01-06', '2020-01-07', '2020-01-08'],
               dtype='datetime64[ns]', freq='D')
```

ここで、 `freq='D'` と表示されているものは、周期を表しています。
 `freq` には次のものを指定できます。

 daterange() で指定できる周期

| コード | 意味 |
|:--|:--|
| D | 日次 Day、デフォルト |
| B | 営業日ごと（平日）, Business Day |
| C | カスタム営業日ごと, Custom Business Day |
| W | 週次, Weekly, W-SUN(Wと同じ),W-MON,W-TUE, W-WED, W-THU, W-FRI, W-SAT |
| M | 月末ごと, Monthly |
| BM | 営業月末ごと, Business Monthly |
| CBM | カスタム営業月末ごと、Custom Business Monthly |
| MS | 月頭ごと Month Start |
| BMS | 営業月頭ごと Business Month Start |
| CBMS | カスタム営業月頭ごと Custom Business Month Start |
| SM | 15日と月末ごと, Semi Monthly |
| SMS | 1日と１５日ごと、Semi Month Start |
| Q | 四半期末ごと, Quarter |
| QS | 四半期頭ごと、Quarter Start |
| BQS | 営業四半期頭ごと、Custom Quarter Start |
| A, Y | 年末ごと, Annualy, Yearly |
| BA, BY | 営業年末ごと、Business Annualy, Business Yearly |  |
| AS, YS | 年頭ごと, Annual Start, Year Start |
| BAS, BYS | 営業年頭ごと, Business Annual Start, Business Year Start |
| H | 時間ごと |
| BH | 営業時間ごと |
| T, min | 分ごと |
| S, s | 秒ごと |
| L, ms | ミリ秒ごと |
| U, us | マイクロ秒ごと |
| N | ナノ秒ごと |
| WOM-... | 毎月第３金曜日であれば WOM-3FRI |

周期を指定した例です。
 Ipython
```
 In [2]: # %load pandas_daterange3.py 
    ...: import pandas as pd 
    ...:  
    ...: dr_1 = pd.date_range('2020-01-01', periods=3, freq='3D') 
    ...: dr_2 = pd.date_range('2020-01-01', periods=3, freq='8H') 
    ...: dr_3 = pd.date_range('2020-01-01', periods=3, freq='4H30min') 
    ...:  
    ...: print(f"freq='3D':\n {dr_1}") 
    ...: print(f"freq='8H':\n {dr_2}") 
    ...: print(f"freq='4H30min':\n {dr_3}") 
    ...:                                                                           
 freq='3D':
  DatetimeIndex(['2020-01-01', '2020-01-04', '2020-01-07'], dtype='datetime64[ns]', freq='3D')
 freq='8H':
  DatetimeIndex(['2020-01-01 00:00:00', '2020-01-01 08:00:00',
                '2020-01-01 16:00:00'],
               dtype='datetime64[ns]', freq='8H')
 freq='4H30min':
  DatetimeIndex(['2020-01-01 00:00:00', '2020-01-01 04:30:00',
                '2020-01-01 09:00:00'],
               dtype='datetime64[ns]', freq='270T')
 
```

 `daterange` を `Series` 型や `DataFrame` 型の `index` にセットして使います。
 Ipython
```
 In [2]: # %load pandas_daterange2.py 
    ...: import pandas as pd 
    ...:  
    ...: dates = pd.date_range(start='2020/1/1', periods=5, freq='D') 
    ...: timeseries = pd.Series(range(5), index=dates) 
    ...:  
    ...: print(timeseries) 
    ...:  
    ...:                                                                           
 2020-01-01    0
 2020-01-02    1
 2020-01-03    2
 2020-01-04    3
 2020-01-05    4
 Freq: D, dtype: int64
```

 `bdate_range()` 関数は、 `date_range()` と違って、 `weekmasks` と `holidays` のキーワード引数を受け取ることができます。

 Ipython
```
 In [2]: # %load pandas_bdaterange.py 
    ...: import datetime 
    ...: import pandas as pd 
    ...:  
    ...: start = datetime.datetime(2020, 1, 1) 
    ...: end = datetime.datetime(2020, 3, 30) 
    ...:  
    ...: weekmask = 'Mon Wed Fri' 
    ...: holidays = [datetime.datetime(2020, 2, 11), 
    ...:             datetime.datetime(2020, 2, 24), 
    ...:             datetime.datetime(2020, 3, 22)] 
    ...:  
    ...: dr_1 = pd.bdate_range(start, end, freq='C', weekmask=weekmask, holidays=ho
    ...: lidays) 
    ...: dr_2 = pd.bdate_range(start, end, freq='CBMS', weekmask=weekmask) 
    ...:  
    ...: print(dr_1) 
    ...: print(dr_2) 
    ...:                                                                           
 DatetimeIndex(['2020-01-01', '2020-01-03', '2020-01-06', '2020-01-08',
                '2020-01-10', '2020-01-13', '2020-01-15', '2020-01-17',
                '2020-01-20', '2020-01-22', '2020-01-24', '2020-01-27',
                '2020-01-29', '2020-01-31', '2020-02-03', '2020-02-05',
                '2020-02-07', '2020-02-10', '2020-02-12', '2020-02-14',
                '2020-02-17', '2020-02-19', '2020-02-21', '2020-02-26',
                '2020-02-28', '2020-03-02', '2020-03-04', '2020-03-06',
                '2020-03-09', '2020-03-11', '2020-03-13', '2020-03-16',
                '2020-03-18', '2020-03-20', '2020-03-23', '2020-03-25',
                '2020-03-27', '2020-03-30'],
               dtype='datetime64[ns]', freq='C')
 DatetimeIndex(['2020-01-01', '2020-02-03', '2020-03-02'], dtype='datetime64[ns]', freq='CBMS')
 
```

参考：
- [Pandas プロジェクト オフィシャルサイト ](https://pandas.pydata.org/)



