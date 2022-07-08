prettypandas を使ってみよう
=================

## PrettyPandasについて
[prettypandas ](https://github.com/HHammond/PrettyPandas) は、シンプルなAPIを使用してレポート品質テーブルを作成するのに便利な、Pandas の DataFrameを拡張したモジュールです。
表形式の出力という意味では逸脱していますが、サマリやAPIの連鎖実行などを利用することで、データ集計のためのコードが簡潔になります。

- サマリを行と列に追加することができる
  - 追加されるメソッド： `total()` 、  `average()` 、  `median()` 、  `min()` 、  `max()` 
- 素敵でカスタマイズ可能なテーマ
- 通貨や科学単位、およびパーセンテージの数値フォーマットが追加される
  - 追加されるメソッド： `as_percent()` 、  `as_currency()` 、  `as_unit()` 
- APIの連鎖実行：オブジェクト指向スタイルでAPIを連続して呼び出せる
- Pandas StyleAPIとシームレスに連携できる


### prettypandas をインストール
prettypandas は拡張モジュールなのでインストールする必要があります。

 bash
```
 $ pip install  prettypandas
```


 using_prettypandas.py
```
 import numpy as np
 import pandas as pd
 from prettypandas import PrettyPandas
 
 teams_list = ["Dallas", "Chicago", "Los Angelos"]
 data = np.array([[1, 2, 1],
                  [0, 1, 0],
                  [2, 4, 1]])
 
 df = pd.DataFrame(data, teams_list, teams_list)
 print( df
       .pipe(PrettyPandas)
       .total(axis=1)
       .average(axis=1)
 )
```

 zsh
```
 % python using_prettypandas.py
              Dallas  Chicago  Los Angelos  Total   Average
 Dallas            1        2            1      4  1.333333
 Chicago           0        1            0      1  0.333333
 Los Angelos       2        4            1      7  2.333333
```


