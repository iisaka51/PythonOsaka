Pandas逆引きレシピ：よく使うコードのまとめ
=================
![](https://gyazo.com/d9aafc28cab8aee408679105533e4661.png)

## はじめに
Pandasはデータ分析のための汎用的で強力なライブラリです。Pandasは、データを扱う様々なタスクに対して非常に多くの便利な関数を提供しています。Pandasを効果的に使うには、いくつかのコツを知っておく必要があります。
この資料は、Pandas でよく使用されるコードをスニペットとしてまとめたものです。

# データセットの準備
 datasets.py
```
 import pandas as pd
 from pathlib import Path
 from urllib.error import HTTPError
 
 class DatasetError(BaseException):
     pass
 
 class DataSet(object):
     baseurl = 'https://raw.githubusercontent.com/adamerose/datasets/master/'
     dataset_names = [
         'anscombe.csv',
         'attention.csv',
         'brain_networks.csv',
         'country_indicators.csv',
         'diamonds.csv',
         'dots.csv',
         'exercise.csv',
         'flights.csv',
         'fmri.csv',
         'gammas.csv',
         'gapminder.csv',
         'geyser.csv',
         'googleplaystore.csv',
          'googleplaystore_reviews.csv',
          'happiness.csv',
          'harry_potter_characters.csv',
          'iris.csv',
          'mi_manufacturing.csv',
          'mpg.csv',
          'netflix_titles.csv',
          'penguins.csv',
          'planets.csv',
          'pokemon.csv',
          'reddit_showerthoughts_may2015.csv',
          'seinfeld_episodes.csv',
          'seinfeld_scripts.csv',
          'stockdata.csv',
          'tips.csv',
          'titanic.csv',
          'trump_tweets.csv',
          'us_shooting_incidents.csv',
      ]
      def load_dataset(self, name, save=False):
          try:
              assert name in self.dataset_names
              exists_flag = Path(name).exists()
              if exists_flag:
                  url = 'file://' + str(Path(name).absolute())
              else:
                  url = self.baseurl + name
              df = pd.read_csv( url )
              _ = save and not exists_flag and df.to_csv(name)
              return df
          except AssertionError:
              raise DatasetError('dataset not available') from None
          except HTTPError as err:
              raise DatasetError(err)
  
      def get_dataset_names(self):
          return self.dataset_names
  dataset = DataSet()
  load_dataset = dataset.load_dataset
  get_dataset_names = dataset.get_dataset_names
  
  
  if __name__ == '__main__':
      import sys
      if len(sys.argv)<=1:
          from pprint import pprint
          pprint(get_dataset_names())
      else:
          _= load_dataset(sys.argv[1], save=True)       
```

 bash
```
 $ python datasets.py stockdata.csv
 $ python datasets.py titanic.csv
```

 stock_datareader.py
```
 from datetime import datetime
 import pandas as pd
 import pandas_datareader as pdr
 
 def load_data(ticker="^GSPC", start=None, end=None, filename=None):
    try:
        start = datetime.fromisoformat(start)
    except:
        start = datetime(datetime.now().year, 1, 1)
    try:
        end = datetime.fromisoformat(end)
    except:
        end = datetime.today()
 
    df = pdr.DataReader(ticker, 'yahoo', start, end)
    _ = filename and df.to_csv(filename)
    return df
 
 if __name__ == '__main__':
     from argparse import ArgumentParser
 
     parser = ArgumentParser(description ='stock data reader')
     parser.add_argument(dest='ticker', metavar='ticker',
                         action='store', nargs=1,
                         help='ticker symbol. i.e.: SP500 is "^GSPC"')
     parser.add_argument('-F', '--filename', metavar='filename',
                         dest='filename', default=None,
                         help='save filename. default is None')
     parser.add_argument('-S', '--start', metavar='YYYY-MM-DD',
                         dest='start', action='store',
                         help='date of start. default is Jan 1st of this year')
     parser.add_argument('-E', '--end', metavar='YYYY-MM-DD',
                         dest='end', action='store',
                         help='date of end. default is today')
 
     args = parser.parse_args()
     load_data(args.ticker[0], args.start, args.end, args.filename)
     
```

 bash
```
 $ python stock_datareader.py -S 2012-01-01 -F TSLA.csv TSLA
```

# Pandas のインポート
以下のスニペットは次のようにPandas をインポートしているものとして記述されています。


```
 import pandas as pd
```

## Pandas の設定情報を取得/変更/リセット


```
 In [2]: # %load c01_pandas_config.py
    ...: import pandas as pd
    ...:
    ...: config = { 'display.max_rows': 100,
    ...:            'display.max_columns': 80,
    ...:            'display.max_colwidth': 20 }
    ...:
    ...: print({x: pd.get_option(x) for x in config.keys()})      # 取得
    ...: _ = [pd.set_option(k,v) for k, v in config.items()]      # 変更
    ...: _ = [pd.reset_option(x) for x in config.keys()]          # リセっっと
    ...:
 {'display.max_rows': 60, 'display.max_columns': 0, 'display.max_colwidth': 50}
 
 In [3]:
 
```

# データを読み込む
 `read_xxx()` を使ってCSV/JSONファイルやEXCELファイルからデータを読み込んでDataFrame を返してくれます。


```
 df = pd.read_csv('csv_file')
 df = pd.read_json('json_file')
 df = pd.read_excel('excel_file') 
```


## 列をフィルタリングして読み込む
データセットから特定の列を取得したいときは、 `usecols()` を使います。


```
 df = pd.read_csv("stockdata.csv", usecols=["date", "stock", "value"])
```



```
 In [2]: # %load c02_usecols.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv("stockdata.csv", usecols=["Date", "stock", "value"])
    ...:
 
 In [3]: df
 Out[3]:
             Date stock        value
 0       1/3/2007  MSFT    23.950705
 1       1/3/2007   IBM    80.517962
 2       1/3/2007  SBUX    16.149666
 3       1/3/2007  AAPL    11.086612
 4       1/3/2007  GSPC  1416.599976
 ...          ...   ...          ...
 11520  2/29/2016  MSFT    50.880001
 11521  2/29/2016   IBM   131.029999
 11522  2/29/2016  SBUX    58.209999
 11523  2/29/2016  AAPL    96.690002
 11524  2/29/2016  GSPC  1932.229980
 
 [11525 rows x 3 columns]
 
 In [4]:
 
```


## 日付の列を指定して読み込む
データセットに日付の列があるときは、読み込み時に指定すると簡単です。


```
 df = pd.read_csv('stockdata.csv', parse_dates=['date'])
```


```
 In [3]: # %load c03_parse_dates.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv("stockdata.csv", parse_dates=["Date"])
 
 In [4]: df
 Out[4]:
        Unnamed: 0       Date stock        value    change
 0               0 2007-01-03  MSFT    23.950705 -0.167452
 1               1 2007-01-03   IBM    80.517962  1.069189
 2               2 2007-01-03  SBUX    16.149666  0.113476
 3               3 2007-01-03  AAPL    11.086612  2.219569
 4               4 2007-01-03  GSPC  1416.599976  0.122829
 ...           ...        ...   ...          ...       ...
 11520       11520 2016-02-29  MSFT    50.880001  3.341197
 11521       11521 2016-02-29   IBM   131.029999  2.549032
 11522       11522 2016-02-29  SBUX    58.209999  3.143793
 11523       11523 2016-02-29  AAPL    96.690002  3.971452
 11524       11524 2016-02-29  GSPC  1932.229980  2.386879
 
 [11525 rows x 5 columns]
 
 In [5]: df.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 11525 entries, 0 to 11524
 Data columns (total 5 columns):
  #   Column      Non-Null Count  Dtype
 ---  ------      --------------  -----
  0   Unnamed: 0  11525 non-null  int64
  1   Date        11525 non-null  datetime64[ns]
  2   stock       11525 non-null  object
  3   value       11525 non-null  float64
  4   change      11525 non-null  float64
 dtypes: datetime64[ns](1), float64(2), int64(1), object(1)
 memory usage: 450.3+ KB
 
 In [6]:
 
```

## データ型を指定して読み込む
読み込み時にカテゴリーデータ型を設定することで、データフレームの使用メモリを大幅に節約することができます。


```
 df = pd.read_csv("stockdata.csv", dtype={"stock": "category"})
```



```
 In [2]: # %load c04_dtype.py
    ...: import pandas as pd
    ...:
    ...: df1 = pd.read_csv('stockdata.csv')
    ...: df2 = pd.read_csv('stockdata.csv', dtype={"stock": "category"})
    ...:
 
 In [3]: df1.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 11525 entries, 0 to 11524
 Data columns (total 5 columns):
  #   Column      Non-Null Count  Dtype
 ---  ------      --------------  -----
  0   Unnamed: 0  11525 non-null  int64
  1   Date        11525 non-null  object
  2   stock       11525 non-null  object
  3   value       11525 non-null  float64
  4   change      11525 non-null  float64
 dtypes: float64(2), int64(1), object(2)
 memory usage: 450.3+ KB
 
 In [4]: df2.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 11525 entries, 0 to 11524
 Data columns (total 5 columns):
  #   Column      Non-Null Count  Dtype
 ---  ------      --------------  -----
  0   Unnamed: 0  11525 non-null  int64
  1   Date        11525 non-null  object
  2   stock       11525 non-null  category
  3   value       11525 non-null  float64
  4   change      11525 non-null  float64
 dtypes: category(1), float64(2), int64(1), object(1)
 memory usage: 371.7+ KB
 
 In [5]:
 
```

## インデックスを設定して読み込む
インデックスを設定することは、特に時系列データで有効です。


```
 df = pd.read_csv("data.csv", index_col="Date")
```



```
 In [2]: # %load c05_index.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('stockdata.csv',
    ...:                  index_col="Date", parse_dates=["Date"])
    ...:
 
 In [3]: df
 Out[3]:
             Unnamed: 0 stock        value    change
 Date
 2007-01-03           0  MSFT    23.950705 -0.167452
 2007-01-03           1   IBM    80.517962  1.069189
 2007-01-03           2  SBUX    16.149666  0.113476
 2007-01-03           3  AAPL    11.086612  2.219569
 2007-01-03           4  GSPC  1416.599976  0.122829
 ...                ...   ...          ...       ...
 2016-02-29       11520  MSFT    50.880001  3.341197
 2016-02-29       11521   IBM   131.029999  2.549032
 2016-02-29       11522  SBUX    58.209999  3.143793
 2016-02-29       11523  AAPL    96.690002  3.971452
 2016-02-29       11524  GSPC  1932.229980  2.386879
 
 [11525 rows x 4 columns]
 
 In [4]: df.info()
 <class 'pandas.core.frame.DataFrame'>
 DatetimeIndex: 11525 entries, 2007-01-03 to 2016-02-29
 Data columns (total 4 columns):
  #   Column      Non-Null Count  Dtype
 ---  ------      --------------  -----
  0   Unnamed: 0  11525 non-null  int64
  1   stock       11525 non-null  object
  2   value       11525 non-null  float64
  3   change      11525 non-null  float64
 dtypes: float64(2), int64(1), object(1)
 memory usage: 450.2+ KB
 
 In [5]:
 
```


## 行数を指定して読み込む
数百万行のデータセットを読み込む前に、それを少し覗いてみたいときは、 `nrows=` で行数を指定できます。


```
 pd.read_csv("stockdata.csv", nrows=10)
```


```
 In [2]: # %load c06_nrows.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv("stockdata.csv", nrows=10)
    ...:
 
 In [3]: df
 Out[3]:
    Unnamed: 0      Date stock        value    change
 0           0  1/3/2007  MSFT    23.950705 -0.167452
 1           1  1/3/2007   IBM    80.517962  1.069189
 2           2  1/3/2007  SBUX    16.149666  0.113476
 3           3  1/3/2007  AAPL    11.086612  2.219569
 4           4  1/3/2007  GSPC  1416.599976  0.122829
 5           5  1/4/2007  MSFT    23.910599 -0.570278
 6           6  1/4/2007   IBM    81.378851 -0.905299
 7           7  1/4/2007  SBUX    16.167992 -0.425056
 8           8  1/4/2007  AAPL    11.332687 -0.712126
 9           9  1/4/2007  GSPC  1418.339966 -0.608458
 
 In [4]:
 
```

## スキップする行を指定して読み込む
データセットに欠陥のあるデータの行があるようなときは、 `skiprows=` でスキップすることができます。


```
 df = pd.read_csv("stockdata.csv", skiprows=[1, 5])  # 1〜5行をスキップ
 
 df = pd.read_csv("stockdata.csv", skiprows=10)     # 先頭から10行をスキップ
 
 skip=lambda x: x > 0 and np.random.rand() > 0.1
 df = pd.read_csv("data.csv", skiprows=skip)         # 全体の90%をランダムにスキップ
```



```
 In [2]: # %load c07_skiprows.py
    ...: import numpy as np
    ...: import pandas as pd
    ...:
    ...: df0 = pd.read_csv("stockdata.csv")
    ...: df1 = pd.read_csv("stockdata.csv", skiprows=[1, 5])
    ...: df2 = pd.read_csv("stockdata.csv", skiprows=10)
    ...:
    ...: skip=lambda x: x > 0 and np.random.rand() > 0.1
    ...: df3 = pd.read_csv("stockdata.csv", skiprows=skip)
    ...:
 
 In [3]: len(df0)
 Out[3]: 11525
 
 In [4]: len(df1)
 Out[4]: 11523
 
 In [5]: len(df2)
 Out[5]: 11515
 
 In [6]: len(df3)
 Out[6]: 1166
 
 In [7]:
```



## 欠損値を指定して読み込む
PythonのPandasはデータ中のNAや空白の値をすべてNaN値として識別します。しかし、na, ?, n.a., n/aを識別しません。
データ中に欠損値と思われる値、例えば `?` が値がある場合、読み込み時に設定することで、後で変換する必要がありません。


```
 df = pd.read_csv('titanic.cssv', na_values=['?']
```



```
 In [2]: # %load c08_na_values.py
    ...: import pandas as pd
    ...: from skimpy import skim
    ...:
    ...: missing_values = ["n/a", "na", " _ _"]
    ...: df = pd.read_csv('titanic.csv', na_values=missing_values)
    ...:
 
 In [3]: df['age']
 Out[3]:
 0     22.000
 1     38.000
 2     26.000
 3     35.000
 4     35.000
        ...
 886   27.000
 887   19.000
 888      NaN
 889   26.000
 890   32.000
 Name: age, dtype: float64
 
 In [4]:
 
```


## ブール値を指定して読み込む
 `yes` /  `no` のようなブール値となるような列があるときは、 `true_values=` と  `false_values=` で指定することができまう。


```
 In [2]: # %load c09_boolean_values.py
    ...: import pandas as pd
    ...:
    ...: df1 = pd.read_csv("titanic.csv")
    ...: df2 = pd.read_csv("titanic.csv",
    ...:                    true_values=["female"], false_values=["male"])
    ...:
    ...: # df1['sex'].head()
    ...: # df2['sex'].head()
    ...:
 
 In [3]: df1['sex'].head()
 Out[3]:
 0      male
 1    female
 2    female
 3    female
 4      male
 Name: sex, dtype: object
 
 In [4]: df2['sex'].head()
 Out[4]:
 0    False
 1     True
 2     True
 3     True
 4    False
 Name: sex, dtype: bool
 
 In [5]:
 
```


## 複数ファイルからの読み込む
データが複数のファイルに分かれているときは、 `glob` でまとめて読み込むことができます。

 bash
```
 $ wc -l stockdata.csv
   11526 stockdata.csv
 $ split -l 3000  stockdata.csv stockdata_
 $ mv stockdata_aa stockdata_aa.csv
 $ mv stockdata_ab stockdata_ab.csv
 $ mv stockdata_ac stockdata_ac.csv
 $ mv stockdata_ad stockdata_ad.csv
 $ wc -l stockdata_*csv
    3000 stockdata_aa.csv
    3000 stockdata_ab.csv
    3000 stockdata_ac.csv
    2526 stockdata_ad.csv
   11526 total
   
```


```
 import glob
 import os
 
 files = glob.glob("stockdata_*.csv")
 df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
```



```
 In [2]: # %load c10_glob_multiple_csv.py
    ...: import glob
    ...: import os
    ...: import pandas as pd
    ...:
    ...: files = glob.glob("stockdata_*.csv")
    ...: df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    ...:
 
 In [3]: df.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 11524 entries, 0 to 11523
 Data columns (total 10 columns):
  #   Column       Non-Null Count  Dtype
 ---  ------       --------------  -----
  0   Unnamed: 0   9999 non-null   float64
  1   Date         9999 non-null   object
  2   stock        9999 non-null   object
  3   value        9999 non-null   float64
  4   change       9999 non-null   float64
  5   9999         1525 non-null   float64
  6   12/10/2014   1525 non-null   object
  7   GSPC         1525 non-null   object
  8   2026.140015  1525 non-null   float64
  9   0.453568901  1525 non-null   float64
 dtypes: float64(6), object(4)
 memory usage: 900.4+ KB
 
 In [4]:
 
```

## データフレームへのコピー＆ペースト
Pandasはクリップボードからデータを読み込むことができます。


```
 df = pd.read_clipboard()
```

## PDFファイルの表から読み込む

[tabula-py ](https://github.com/chezou/tabula-py) を使うと、PDFの表から読み込むことができます。


```
 # %pip install tabula-py
 from tabula import read_pdf
 df = read_pdf('test.pdf', pages='all')
```


# フィルタリング
## データ型を指定してフィルタリング
Pandasで定義されている [データ型 ](https://pandas.pydata.org/pandas-docs/stable/user_guide/basics.html#basics-dtypes) を指定してフィルタリングすることができます。


```
 df1 = df.select_dtypes(include="float64")
 df2 = df.select_dtypes(include=["category", "int64"])
 df3 = df.select_dtypes(exclude="int64")
```





```
 In [2]: # %load c11_filtering_dtype.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('stockdata.csv',
    ...:                  dtype={"stock": "category"},
    ...:                  index_col="Date", parse_dates=["Date"])
    ...:
    ...: df1 = df.select_dtypes(include="float64")
    ...: df2 = df.select_dtypes(include=["category", "int64"])
    ...: df3 = df.select_dtypes(exclude="int64")
    ...:
 
 In [3]: df1
 Out[3]:
                   value    change
 Date
 2007-01-03    23.950705 -0.167452
 2007-01-03    80.517962  1.069189
 2007-01-03    16.149666  0.113476
 2007-01-03    11.086612  2.219569
 2007-01-03  1416.599976  0.122829
 ...                 ...       ...
 2016-02-29    50.880001  3.341197
 2016-02-29   131.029999  2.549032
 2016-02-29    58.209999  3.143793
 2016-02-29    96.690002  3.971452
 2016-02-29  1932.229980  2.386879
 
 [11525 rows x 2 columns]
 
 In [4]: df2
 Out[4]:
             Unnamed: 0 stock
 Date
 2007-01-03           0  MSFT
 2007-01-03           1   IBM
 2007-01-03           2  SBUX
 2007-01-03           3  AAPL
 2007-01-03           4  GSPC
 ...                ...   ...
 2016-02-29       11520  MSFT
 2016-02-29       11521   IBM
 2016-02-29       11522  SBUX
 2016-02-29       11523  AAPL
 2016-02-29       11524  GSPC
 
 [11525 rows x 2 columns]
 
 In [5]: df3
 Out[5]:
            stock        value    change
 Date
 2007-01-03  MSFT    23.950705 -0.167452
 2007-01-03   IBM    80.517962  1.069189
 2007-01-03  SBUX    16.149666  0.113476
 2007-01-03  AAPL    11.086612  2.219569
 2007-01-03  GSPC  1416.599976  0.122829
 ...          ...          ...       ...
 2016-02-29  MSFT    50.880001  3.341197
 2016-02-29   IBM   131.029999  2.549032
 2016-02-29  SBUX    58.209999  3.143793
 2016-02-29  AAPL    96.690002  3.971452
 2016-02-29  GSPC  1932.229980  2.386879
 
 [11525 rows x 3 columns]
 
 In [6]:
 
```

## ダウンキャスト
Pandasの `to_numeric()` には、型をダウンキャストする機能があり、データフレームのサイズを小さくすることができます。


```
 df1['Unnamed: 0'] = pd.to_numeric(df1['Unnamed: 0'], downcast="integer")
 df1['value'] = pd.to_numeric(df1['value'], downcast="float")
 df1['change'] = pd.to_numeric(df1['change'], downcast="float")
 
```



```
 In [2]: # %load c12_downcast.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('stockdata.csv')
    ...:
    ...: df1 = df.copy()
    ...: df1['Unnamed: 0'] = pd.to_numeric(df1['Unnamed: 0'], downcast="integer")
    ...:
    ...: df1['value'] = pd.to_numeric(df1['value'], downcast="float")
    ...: df1['change'] = pd.to_numeric(df1['change'], downcast="float")
    ...:
    ...:
 
 In [3]: df.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 11525 entries, 0 to 11524
 Data columns (total 5 columns):
  #   Column      Non-Null Count  Dtype
 ---  ------      --------------  -----
  0   Unnamed: 0  11525 non-null  int64
  1   Date        11525 non-null  object
  2   stock       11525 non-null  object
  3   value       11525 non-null  float64
  4   change      11525 non-null  float64
 dtypes: float64(2), int64(1), object(2)
 memory usage: 450.3+ KB
 
 In [4]: df1.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 11525 entries, 0 to 11524
 Data columns (total 5 columns):
  #   Column      Non-Null Count  Dtype
 ---  ------      --------------  -----
  0   Unnamed: 0  11525 non-null  int16
  1   Date        11525 non-null  object
  2   stock       11525 non-null  object
  3   value       11525 non-null  float32
  4   change      11525 non-null  float32
 dtypes: float32(2), int16(1), object(2)
 memory usage: 292.8+ KB
 
 In [5]:
 
```

## 手動変換
データ中に欠損値がある場合、 `errors="coerce"` を使用すると、それらの厄介なエラーを防ぐことができます。同時に、 `.fillna` を使って、これらの欠損値を妥当な値で埋めることができます。


```
 df1 = df1.apply(pd.to_numeric, errors="coerce")
 
 df2 = df.copy()
 # 指定した列を変換
 df2.age = pd.to_numeric(df2.age, errors="coerce")
 
 df3 = df.copy()
 # 欠損値をゼロ(0)で埋める
 df3.age = pd.to_numeric(df3.age, errors="coerce").fillna(0)
```



```
 In [2]: # %load c13_fillna.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...: df1 = df.copy()
    ...:
    ...: # データフレーム全体を変換
    ...: df1 = df1.apply(pd.to_numeric, errors="coerce")
    ...:
    ...: df2 = df.copy()
    ...: # 指定した列を変換
    ...: df2.age = pd.to_numeric(df2.age, errors="coerce")
    ...:
    ...: df3 = df.copy()
    ...: # 欠損値をゼロ(0)で埋める
    ...: df3.age = pd.to_numeric(df3.age, errors="coerce").fillna(0)
    ...:
    ...: # df1
    ...: # df2.age
    ...: # df3.age
    ...:
 
 In [3]: df1
 Out[3]:
      Unnamed: 0  survived  pclass  sex  ...  deck  embark_town  alive  alone
 0             0         0       3  NaN  ...   NaN          NaN    NaN  False
 1             1         1       1  NaN  ...   NaN          NaN    NaN  False
 2             2         1       3  NaN  ...   NaN          NaN    NaN   True
 3             3         1       1  NaN  ...   NaN          NaN    NaN  False
 4             4         0       3  NaN  ...   NaN          NaN    NaN   True
 ..          ...       ...     ...  ...  ...   ...          ...    ...    ...
 886         886         0       2  NaN  ...   NaN          NaN    NaN   True
 887         887         1       1  NaN  ...   NaN          NaN    NaN   True
 888         888         0       3  NaN  ...   NaN          NaN    NaN  False
 889         889         1       1  NaN  ...   NaN          NaN    NaN   True
 890         890         0       3  NaN  ...   NaN          NaN    NaN   True
 
 [891 rows x 16 columns]
 
 In [4]: df2.age
 Out[4]:
 0      22.0
 1      38.0
 2      26.0
 3      35.0
 4      35.0
        ...
 886    27.0
 887    19.0
 888     NaN
 889    26.0
 890    32.0
 Name: age, Length: 891, dtype: float64
 
 In [5]: df3.age
 Out[5]:
 0      22.0
 1      38.0
 2      26.0
 3      35.0
 4      35.0
        ...
 886    27.0
 887    19.0
 888     0.0
 889    26.0
 890    32.0
 Name: age, Length: 891, dtype: float64
 
 In [6]:
 
```

## データ型を一括で変換


```
 df = df.astype(
     {
         "Date": "datetime64[ns]",
         "stock": "category",
         "value": "float",
         "change": "float",
     }
 )
 
```



```
 In [2]: # %load c14_convert_at_once.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('stockdata.csv')
    ...:
    ...: df = df.astype(
    ...:     {
    ...:         "Date": "datetime64[ns]",
    ...:         "stock": "category",
    ...:         "value": "float",
    ...:         "change": "float",
    ...:     }
    ...: )
    ...:
 
 In [3]: df
 Out[3]:
        Unnamed: 0       Date stock        value    change
 0               0 2007-01-03  MSFT    23.950705 -0.167452
 1               1 2007-01-03   IBM    80.517962  1.069189
 2               2 2007-01-03  SBUX    16.149666  0.113476
 3               3 2007-01-03  AAPL    11.086612  2.219569
 4               4 2007-01-03  GSPC  1416.599976  0.122829
 ...           ...        ...   ...          ...       ...
 11520       11520 2016-02-29  MSFT    50.880001  3.341197
 11521       11521 2016-02-29   IBM   131.029999  2.549032
 11522       11522 2016-02-29  SBUX    58.209999  3.143793
 11523       11523 2016-02-29  AAPL    96.690002  3.971452
 11524       11524 2016-02-29  GSPC  1932.229980  2.386879
 
 [11525 rows x 5 columns]
 
 In [4]: df.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 11525 entries, 0 to 11524
 Data columns (total 5 columns):
  #   Column      Non-Null Count  Dtype
 ---  ------      --------------  -----
  0   Unnamed: 0  11525 non-null  int64
  1   Date        11525 non-null  datetime64[ns]
  2   stock       11525 non-null  category
  3   value       11525 non-null  float64
  4   change      11525 non-null  float64
 dtypes: category(1), datetime64[ns](1), float64(2), int64(1)
 memory usage: 371.7 KB
 
 In [5]:
 
```


# 列を操作

## 列名を変更 rename()
 `rename()` メソッドで変更する列と変更後の列名を辞書で与えます。


```
 df = df.rename({"value": "price", "Date": "date"}, axis=1)
```


```
 In [2]: # %load c15_col_rename.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('stockdata.csv')
    ...:
    ...: df = df.rename({"value": "price", "Date": "date"}, axis=1)
    ...:
 
 In [3]: df.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 11525 entries, 0 to 11524
 Data columns (total 5 columns):
  #   Column      Non-Null Count  Dtype
 ---  ------      --------------  -----
  0   Unnamed: 0  11525 non-null  int64
  1   date        11525 non-null  object
  2   stock       11525 non-null  object
  3   price       11525 non-null  float64
  4   change      11525 non-null  float64
 dtypes: float64(2), int64(1), object(2)
 memory usage: 450.3+ KB
 
 In [4]:
 
```

## 列名の変更 文字列操作
一般的な文字列操作で列名を変更することができます。


```
 df.columns = df.columns.str.upper()   # 大文字へ変換
 df.columns = df.columns.str.replace('alive', 'Alive')
 
```


```
 In [2]: # %load c16_rename_as_str.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...:
    ...: v1 = df.columns
    ...: v2 = df.columns.str.upper()
    ...: v3 = df.columns.str.replace('survived', 'SURVIVED')
    ...:
    ...: df.columns = v2
    ...:
 
 In [3]: v1
 Out[3]:
 Index(['Unnamed: 0', 'survived', 'pclass', 'sex', 'age', 'sibsp', 'parch',
        'fare', 'embarked', 'class', 'who', 'adult_male', 'deck', 'embark_town',
        'alive', 'alone'],
       dtype='object')
 
 In [4]: v2
 Out[4]:
 Index(['UNNAMED: 0', 'SURVIVED', 'PCLASS', 'SEX', 'AGE', 'SIBSP', 'PARCH',
        'FARE', 'EMBARKED', 'CLASS', 'WHO', 'ADULT_MALE', 'DECK', 'EMBARK_TOWN',
        'ALIVE', 'ALONE'],
       dtype='object')
 
 In [5]: v3
 Out[5]:
 Index(['Unnamed: 0', 'SURVIVED', 'pclass', 'sex', 'age', 'sibsp', 'parch',
        'fare', 'embarked', 'class', 'who', 'adult_male', 'deck', 'embark_town',
        'alive', 'alone'],
       dtype='object')
 
 In [6]: df.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 891 entries, 0 to 890
 Data columns (total 16 columns):
  #   Column       Non-Null Count  Dtype
 ---  ------       --------------  -----
  0   UNNAMED: 0   891 non-null    int64
  1   SURVIVED     891 non-null    int64
  2   PCLASS       891 non-null    int64
  3   SEX          891 non-null    object
  4   AGE          714 non-null    float64
  5   SIBSP        891 non-null    int64
  6   PARCH        891 non-null    int64
  7   FARE         891 non-null    float64
  8   EMBARKED     889 non-null    object
  9   CLASS        891 non-null    object
  10  WHO          891 non-null    object
  11  ADULT_MALE   891 non-null    bool
  12  DECK         203 non-null    object
  13  EMBARK_TOWN  889 non-null    object
  14  ALIVE        891 non-null    object
  15  ALONE        891 non-null    bool
 dtypes: bool(2), float64(2), int64(5), object(7)
 memory usage: 99.3+ KB
 
 In [7]:
 
```

## 列名にprefix や suffix を追加
 `add_prefix()` 、 `add_suffix()` メソッドで列名の前後に文字列を追加することができます。


```
 df.add_prefix("pre_")
 df.add_suffix("_suf")
```


```
 In [2]: # %load c17_prefix_suffix.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('stockdata.csv')
    ...:
    ...: df = df.add_prefix('PRE_')
    ...: df = df.add_suffix('_SUF')
    ...:
 
 In [3]: df.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 11525 entries, 0 to 11524
 Data columns (total 5 columns):
  #   Column              Non-Null Count  Dtype
 ---  ------              --------------  -----
  0   PRE_Unnamed: 0_SUF  11525 non-null  int64
  1   PRE_Date_SUF        11525 non-null  object
  2   PRE_stock_SUF       11525 non-null  object
  3   PRE_value_SUF       11525 non-null  float64
  4   PRE_change_SUF      11525 non-null  float64
 dtypes: float64(2), int64(1), object(2)
 memory usage: 450.3+ KB
 
 In [4]:
 
```


命名ルールに適用させるために、列名を変更したくなることがあります。特にデータベースへ書き出したいようなときはフィールド名と列名を同じにしたいときなどです。
一般によく使用される命名ツールには次のようなものがあります。

 命名ルール

| 呼称 | 例 |
|:--|:--|
| snake case | column_name |
| kebab case  | column-name |
| camel case | columnName |
| pascal case | ColumnName |
| const case | COLUMN_NAME |
| sentence | Column name |
| title | Column Name' |
| lower case | 'column name |
| upper case | COLUMN NAME |

## 列の追加
データフレームの列を追加する方法はいくつかあります。

### 条件式の結果で列を追加する loc()
 `loc()` メソッドで列を追加することができます。次のような書式で指定します。


```
 df.loc[df['列名'] 条件式, '新しい列名'] = '条件式が真のときの値'
```


```
 In [2]: # %load c18_create_col_condition.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...:
    ...: df.loc[df['sex'] == 'female', 'sex_flag'] = 'True'
    ...: df.loc[df['sex'] == 'male', 'sex_flag'] = 'False'
    ...:
 
 In [3]: df.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 891 entries, 0 to 890
 Data columns (total 17 columns):
  #   Column       Non-Null Count  Dtype
 ---  ------       --------------  -----
  0   Unnamed: 0   891 non-null    int64
  1   survived     891 non-null    int64
  2   pclass       891 non-null    int64
  3   sex          891 non-null    object
  4   age          714 non-null    float64
  5   sibsp        891 non-null    int64
  6   parch        891 non-null    int64
  7   fare         891 non-null    float64
  8   embarked     889 non-null    object
  9   class        891 non-null    object
  10  who          891 non-null    object
  11  adult_male   891 non-null    bool
  12  deck         203 non-null    object
  13  embark_town  889 non-null    object
  14  alive        891 non-null    object
  15  alone        891 non-null    bool
  16  sex_flag     891 non-null    object
 dtypes: bool(2), float64(2), int64(5), object(8)
 memory usage: 106.3+ KB
 
 In [4]: df['sex_flag']
 Out[4]:
 0      False
 1       True
 2       True
 3       True
 4      False
        ...
 886    False
 887     True
 888     True
 889    False
 890    False
 Name: sex_flag, Length: 891, dtype: object
 
 In [5]:
 
```


### 条件式の結果で列を追加する apply
 `apply()` メソッドで列の値に対して条件式を適用した結果からカ列を追加することができます。次のような書式で指定します。


```
 df['新しい列名'] = df['列名'].apply(lambda x: 条件式が真のときの値 if x 条件式 else 条件式が偽のときの値)
```


```
 In [2]: # %load c19_create_col_apply.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...:
    ...: is_female = lambda x: 'True' if x == 'female' else 'False'
    ...: df['sex_flag'] = df['sex'].apply(is_female)
    ...:
 
 In [3]: df.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 891 entries, 0 to 890
 Data columns (total 17 columns):
  #   Column       Non-Null Count  Dtype
 ---  ------       --------------  -----
  0   Unnamed: 0   891 non-null    int64
  1   survived     891 non-null    int64
  2   pclass       891 non-null    int64
  3   sex          891 non-null    object
  4   age          714 non-null    float64
  5   sibsp        891 non-null    int64
  6   parch        891 non-null    int64
  7   fare         891 non-null    float64
  8   embarked     889 non-null    object
  9   class        891 non-null    object
  10  who          891 non-null    object
  11  adult_male   891 non-null    bool
  12  deck         203 non-null    object
  13  embark_town  889 non-null    object
  14  alive        891 non-null    object
  15  alone        891 non-null    bool
  16  sex_flag     891 non-null    object
 dtypes: bool(2), float64(2), int64(5), object(8)
 memory usage: 106.3+ KB
 
 In [4]: df['sex_flag']
 Out[4]:
 0      False
 1       True
 2       True
 3       True
 4      False
        ...
 886    False
 887     True
 888     True
 889    False
 890    False
 Name: sex_flag, Length: 891, dtype: object
 
 In [5]:
 
```

## lambda式を列に適用した結果を追加する assign()
摂氏から華氏の値の新しい列を作成する場合は次のようにします。


```
 df.assign(temp_f=lambda x: x.temp_c * 9 / 5 + 32)
```


## 列の値に条件式を適用した結果を追加する np.where()


```
 df["sex_flag"] = np.where(df["sex"] == "female", "True", "False")
```


```
 In [2]: # %load c20_create_col_where.py
    ...: import pandas as pd
    ...: import numpy as np
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...:
    ...: df['sex_flag'] = np.where(df['sex'] == 'female', 'True', 'False')
    ...:
 
 In [3]: df.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 891 entries, 0 to 890
 Data columns (total 17 columns):
  #   Column       Non-Null Count  Dtype
 ---  ------       --------------  -----
  0   Unnamed: 0   891 non-null    int64
  1   survived     891 non-null    int64
  2   pclass       891 non-null    int64
  3   sex          891 non-null    object
  4   age          714 non-null    float64
  5   sibsp        891 non-null    int64
  6   parch        891 non-null    int64
  7   fare         891 non-null    float64
  8   embarked     889 non-null    object
  9   class        891 non-null    object
  10  who          891 non-null    object
  11  adult_male   891 non-null    bool
  12  deck         203 non-null    object
  13  embark_town  889 non-null    object
  14  alive        891 non-null    object
  15  alone        891 non-null    bool
  16  sex_flag     891 non-null    object
 dtypes: bool(2), float64(2), int64(5), object(8)
 memory usage: 106.3+ KB
 
 In [4]: df['sex_flag']
 Out[4]:
 0      False
 1       True
 2       True
 3       True
 4      False
        ...
 886    False
 887     True
 888     True
 889    False
 890    False
 Name: sex_flag, Length: 891, dtype: object
 
 In [5]:
 
```

## 指定した位置に列を挿入
 `insert()` メソッドを使うと指定した位置に列を挿入することができます。


```
 random_col = np.random.randint(10, size=len(df))
 df.insert(3, 'random_col', random_col) 
```


```
 In [2]: # %load c21_insert_col.py
    ...: import numpy as np
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('stockdata.csv')
    ...:
    ...: random_col = np.random.randint(10, size=len(df))
    ...: df.insert(3, 'random_col', random_col)
    ...:
 
 In [3]: df.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 11525 entries, 0 to 11524
 Data columns (total 6 columns):
  #   Column      Non-Null Count  Dtype
 ---  ------      --------------  -----
  0   Unnamed: 0  11525 non-null  int64
  1   Date        11525 non-null  object
  2   stock       11525 non-null  object
  3   random_col  11525 non-null  int64
  4   value       11525 non-null  float64
  5   change      11525 non-null  float64
 dtypes: float64(2), int64(2), object(2)
 memory usage: 540.4+ KB
 
 In [4]:
 
```


## 列の削除
列の削除もいくつかの方法があります。

### 列を削除したデータフレームを取得
 `drop()` メソッドで削除するラベルをリストで与えます。 `axis=1` を与えると列が対象となり、ラベルは列名になります。
デフォルトでは `axis` はゼロ( `0` )で行が対象となり、ソースのDataFrameは変更されず、新しいDataFrameが返されることに注意してください。


```
 df = df.drop['col1', 'col2'], axis=1)
```


```
 In [2]: # %load c22_drop_col.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...:
    ...: df1 = df.drop(['Unnamed: 0', 'who', 'embark_town'], axis=1)
    ...:
 
 In [3]: df.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 891 entries, 0 to 890
 Data columns (total 16 columns):
  #   Column       Non-Null Count  Dtype
 ---  ------       --------------  -----
  0   Unnamed: 0   891 non-null    int64
  1   survived     891 non-null    int64
  2   pclass       891 non-null    int64
  3   sex          891 non-null    object
  4   age          714 non-null    float64
  5   sibsp        891 non-null    int64
  6   parch        891 non-null    int64
  7   fare         891 non-null    float64
  8   embarked     889 non-null    object
  9   class        891 non-null    object
  10  who          891 non-null    object
  11  adult_male   891 non-null    bool
  12  deck         203 non-null    object
  13  embark_town  889 non-null    object
  14  alive        891 non-null    object
  15  alone        891 non-null    bool
 dtypes: bool(2), float64(2), int64(5), object(7)
 memory usage: 99.3+ KB
 
 In [4]: df1.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 891 entries, 0 to 890
 Data columns (total 13 columns):
  #   Column      Non-Null Count  Dtype
 ---  ------      --------------  -----
  0   survived    891 non-null    int64
  1   pclass      891 non-null    int64
  2   sex         891 non-null    object
  3   age         714 non-null    float64
  4   sibsp       891 non-null    int64
  5   parch       891 non-null    int64
  6   fare        891 non-null    float64
  7   embarked    889 non-null    object
  8   class       891 non-null    object
  9   adult_male  891 non-null    bool
  10  deck        203 non-null    object
  11  alive       891 non-null    object
  12  alone       891 non-null    bool
 dtypes: bool(2), float64(2), int64(4), object(5)
 memory usage: 78.4+ KB
 
 In [5]:
 
```

### データフレームから列を削除する
上記の例とほとんど同じですが、 `inplace=True` を与えるとソースのデータフレームに対して処理されます。


```
 df.drop('col1', axis=1, inplace=True)
```


```
 In [2]: # %load c23_drop_col_inplace.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...:
    ...: df.drop(['Unnamed: 0', 'who', 'embark_town'], axis=1, inplace=True)
    ...:
 
 In [3]: df.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 891 entries, 0 to 890
 Data columns (total 13 columns):
  #   Column      Non-Null Count  Dtype
 ---  ------      --------------  -----
  0   survived    891 non-null    int64
  1   pclass      891 non-null    int64
  2   sex         891 non-null    object
  3   age         714 non-null    float64
  4   sibsp       891 non-null    int64
  5   parch       891 non-null    int64
  6   fare        891 non-null    float64
  7   embarked    889 non-null    object
  8   class       891 non-null    object
  9   adult_male  891 non-null    bool
  10  deck        203 non-null    object
  11  alive       891 non-null    object
  12  alone       891 non-null    bool
 dtypes: bool(2), float64(2), int64(4), object(5)
 memory usage: 78.4+ KB
 
 In [4]:
 
```

# 値の検索

## 文字列操作として検索 contains()


```
 df['name'].str.contains("Freddie")
 df['phone_num'].str.contains('...-...-....', regex=True) 
```


```
 In [2]: # %load c30_str_contains.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...:
    ...: v1 = df['embark_town']
    ...: v2 = df['embark_town'].str.contains('town')
    ...: v3 = df['embark_town'].str.contains('^Q.*', regex=True)
    ...:
 
 In [3]: v1
 Out[3]:
 0      Southampton
 1        Cherbourg
 2      Southampton
 3      Southampton
 4      Southampton
           ...
 886    Southampton
 887    Southampton
 888    Southampton
 889      Cherbourg
 890     Queenstown
 Name: embark_town, Length: 891, dtype: object
 
 In [4]: v2
 Out[4]:
 0      False
 1      False
 2      False
 3      False
 4      False
        ...
 886    False
 887    False
 888    False
 889    False
 890     True
 Name: embark_town, Length: 891, dtype: object
 
 In [5]: v3
 Out[5]:
 0      False
 1      False
 2      False
 3      False
 4      False
        ...
 886    False
 887    False
 888    False
 889    False
 890     True
 Name: embark_town, Length: 891, dtype: object
 
 In [6]:
 
```

## 文字列操作として検索 findall()
 `contains()` でも正規表現で検索できますが、 `findall()` では re モジュールのフラグを与えることができるので、大文字小文字を問わずに検索するようなときは、パターンの指定が簡単になります。 `contains()` ではヒットしたかどうかの審議地を返しますが、 `findall()` では、パターンに合致する文字列を返すことに注意してください。


```
 import re
 df['col1'].str.findall(regexp, flags=re.IGNORECASE)
```


```
 In [2]: # %load c31_str_findall.py
    ...: import pandas as pd
    ...: import re
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...:
    ...: regexp = '^Q.*'
    ...: v1 = df['embark_town'].str.findall(regexp, flags=re.IGNORECASE)
    ...:
 
 In [3]: v1
 Out[3]:
 0                []
 1                []
 2                []
 3                []
 4                []
            ...
 886              []
 887              []
 888              []
 889              []
 890    [Queenstown]
 Name: embark_town, Length: 891, dtype: object
 
 In [4]:
 
```


# 欠損値
データセットに存在するかもしれない欠損値を把握することはデータ分析では非常に重要です。

## 欠損値があるかをチェック isnull()
データフレームに欠損値があるかどうかを単純に調べるときは  `isnull()` を使います。


```
 df.isnull()
 df['col1'].isnull()
 df['col1'].isnull().values.any()
```



```
 
 In [2]: # %load c40_missing_val_isnull.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...:
    ...: v1 = df.isnull()
    ...: v2 = df['age'].isnull()
    ...: v3 = df['age'].isnull().values[:10]
    ...: v4 = df['age'].isnull().values.any()
    ...:
 
 In [3]: v1
 Out[3]:
      Unnamed: 0  survived  pclass    sex  ...   deck  embark_town  alive  alone
 0         False     False   False  False  ...   True        False  False  False
 1         False     False   False  False  ...  False        False  False  False
 2         False     False   False  False  ...   True        False  False  False
 3         False     False   False  False  ...  False        False  False  False
 4         False     False   False  False  ...   True        False  False  False
 ..          ...       ...     ...    ...  ...    ...          ...    ...    ...
 886       False     False   False  False  ...   True        False  False  False
 887       False     False   False  False  ...  False        False  False  False
 888       False     False   False  False  ...   True        False  False  False
 889       False     False   False  False  ...  False        False  False  False
 890       False     False   False  False  ...   True        False  False  False
 
 [891 rows x 16 columns]
 
 In [4]: v2
 Out[4]:
 0      False
 1      False
 2      False
 3      False
 4      False
        ...
 886    False
 887    False
 888     True
 889    False
 890    False
 Name: age, Length: 891, dtype: bool
 
 In [5]: v3
 Out[5]:
 array([False, False, False, False, False,  True, False, False, False,
        False])
 
 In [6]: v4
 Out[6]: True
 
 In [7]:
 
```


## 欠損値をカウントする
 `isnull()` が返すオブジェクトで  `sum()` メソッドを呼び出すと、欠損値をカウントすsることができます。


```
 df.isnull().sum()
 df.isnull().sum().sum()
 df['col'].isnull().sum()
```


```
 In [2]: # %load c41_missing_val_counting.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...:
    ...: v1 = df.isnull().sum()
    ...: v2 = df.isnull().sum().sum()
    ...: v3 = df['age'].isnull().sum()
    ...:
 
 In [3]: v1
 Out[3]:
 Unnamed: 0       0
 survived         0
 pclass           0
 sex              0
 age            177
 sibsp            0
 parch            0
 fare             0
 embarked         2
 class            0
 who              0
 adult_male       0
 deck           688
 embark_town      2
 alive            0
 alone            0
 dtype: int64
 
 In [4]: v2
 Out[4]: 869
 
 In [5]: v3
 Out[5]: 177
 
 In [6]:
 
```

## 欠損値を調整する

### 欠損値を削除する
 `dropna()` 欠損値を削除することができます。  `axis=0` で欠損値を含む行を削除、 `axis=1` で欠損値を含む列を削除します。


```
 newdf = df.dropna(axis=0)
 newdf = df.dropna(axis=1)
```


```
 In [2]: # %load c42_missing_val_drop.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...:
    ...: v1 = df.isnull().sum()
    ...:
    ...: df1 = df.dropna(axis=0)
    ...: v2 = df1.isnull().sum()
    ...:
    ...: df2 = df.dropna(axis=1)
    ...: v3 = df2.isnull().sum()
    ...:
 
 In [3]: v1
 Out[3]:
 Unnamed: 0       0
 survived         0
 pclass           0
 sex              0
 age            177
 sibsp            0
 parch            0
 fare             0
 embarked         2
 class            0
 who              0
 adult_male       0
 deck           688
 embark_town      2
 alive            0
 alone            0
 dtype: int64
 
 In [4]: v2
 Out[4]:
 Unnamed: 0     0
 survived       0
 pclass         0
 sex            0
 age            0
 sibsp          0
 parch          0
 fare           0
 embarked       0
 class          0
 who            0
 adult_male     0
 deck           0
 embark_town    0
 alive          0
 alone          0
 dtype: int64
 
 In [5]: v3
 Out[5]:
 Unnamed: 0    0
 survived      0
 pclass        0
 sex           0
 sibsp         0
 parch         0
 fare          0
 class         0
 who           0
 adult_male    0
 alive         0
 alone         0
 dtype: int64
 
 In [6]:
 
```

この方法は、欠損値のあるデータを完全に削除することで、ロバストで精度の高いモデルになります。しかし、情報やデータの損失を伴うことに注意してください。データセット全体と比較して、欠損値の割合が高い場合（例えば30％）では、分析に悪影響を与える可能性が’高くなります。


## 欠損値を置き換える


```
 df.replace( -999999, np.nan)
 df.replace("?", np.nan)
```


## 欠損値を特定の値あるいは前後のデータでうめる fillna()


```
 df.fillna(0)
 
 df.fillna(method="ffill")
 df.fillna(method='bfill')
  
 sr_age = df['age']
 df['age'].fillna(sr_age.mean())
 df['age'].fillna(sr_age.median())
 df['age'].fillna(sr_age.mode().to_list()[0])
 
```



```
 In [2]: # %load c43_missing_val_fillna.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...:
    ...: v1 = df['age']
    ...: v2 = df['age'].fillna(0)
    ...: v3 = df['age'].fillna(method='ffill')
    ...: v4 = df['age'].fillna(method='bfill')
    ...:
    ...: v_avg = df['age'].fillna(v1.mean())
    ...: v_median = df['age'].fillna(v1.median())
    ...: v_mode = df['age'].fillna(v1.mode().to_list()[0])
    ...:
 
 In [3]: v1
 Out[3]:
 0     22.000
 1     38.000
 2     26.000
 3     35.000
 4     35.000
        ...
 886   27.000
 887   19.000
 888      NaN
 889   26.000
 890   32.000
 Name: age, dtype: float64
 
 In [4]: v2
 Out[4]:
 0     22.000
 1     38.000
 2     26.000
 3     35.000
 4     35.000
        ...
 886   27.000
 887   19.000
 888    0.000
 889   26.000
 890   32.000
 Name: age, dtype: float64
 
 In [5]: v3
 Out[5]:
 0     22.000
 1     38.000
 2     26.000
 3     35.000
 4     35.000
        ...
 886   27.000
 887   19.000
 888   19.000
 889   26.000
 890   32.000
 Name: age, dtype: float64
 
 In [6]: v4
 Out[6]:
 0     22.000
 1     38.000
 2     26.000
 3     35.000
 4     35.000
        ...
 886   27.000
 887   19.000
 888   26.000
 889   26.000
 890   32.000
 Name: age, dtype: float64
 
 In [7]: v_avg[888]
 Out[7]: 29.69911764705882
 
 In [8]: v_median[888]
 Out[8]: 28.0
 
 In [9]: v_mode[888]
 Out[9]: 24.0
 
 In [10]:
 
```

 `fillna()` は `dropna()` と違い行や列が削除されるようなデータ損失を防ぐことができることから、データサイズが小さい場合、この方法が適していると言えます。しかし、平均値、中央値、歳頻値などと置き換えるために、分散にバイアスがかかってしまうことに注意してください。
 `fillna()` に与える `method=ffill` は、Next Observation Carried Backward(NOCB) と呼ばれる方法で、データ列の次の値を使って充当するものです。 `method=bfill` は、Last Observation Carried Forward (LOCF) と呼ばれる方法で、データ列のひとつ前の値を使って充当するものです


## データを補間する interpolate()

#### 線形補間（Linear Interpolation）
#### スプライン補間（spline interpolation）
]

```
 df.interpolate(method='linear')
 df.interpolate(method='spline')
```


```
 In [1]: # %load c44_missing_val_interpolate.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...:
    ...: v1 = df['age']
    ...: v2 = df['age'].interpolate(method='linear')
    ...: v3 = df['age'].interpolate(option='spline')
 
 In [2]: v1[880:]
 Out[2]:
 880   25.000
 881   33.000
 882   22.000
 883   28.000
 884   25.000
 885   39.000
 886   27.000
 887   19.000
 888      NaN
 889   26.000
 890   32.000
 Name: age, dtype: float64
 
 In [3]: v2[880:]
 Out[3]:
 880   25.000
 881   33.000
 882   22.000
 883   28.000
 884   25.000
 885   39.000
 886   27.000
 887   19.000
 888   22.500
 889   26.000
 890   32.000
 Name: age, dtype: float64
 
 In [4]: v3[880:]
 Out[4]:
 880   25.000
 881   33.000
 882   22.000
 883   28.000
 884   25.000
 885   39.000
 886   27.000
 887   19.000
 888   22.500
 889   26.000
 890   32.000
 Name: age, dtype: float64
 
 In [5]:
 
```

## 欠損値の割合を知る


```
 In [2]: # %load c45_check_missing_value.py
    ...: import pandas as pd
    ...:
    ...: def missing_rate(df):
    ...:     missing = [
    ...:         (df.columns[idx], perc)
    ...:         for idx, perc in enumerate(df.isna().mean() * 100)
    ...:         if perc > 0
    ...:     ]
    ...:
    ...:     if len(missing) == 0:
    ...:         return "no missing values"
    ...:
    ...:     missing.sort(key=lambda x: x[1], reverse=True)
    ...:
    ...:     print(f"Total of {len(missing)} variables with missing values\n")
    ...:     for label, pct in missing:
    ...:         print(str.ljust(f"{label:<20} => {round(pct, 3)}%", 1))
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...: missing_rate(df)
    ...:
 Total of 4 variables with missing values
 
 deck                 => 77.217%
 age                  => 19.865%
 embarked             => 0.224%
 embark_town          => 0.224%
 
 In [3]:
```


# 日時処理

Pandas では時系列処理ができることもあり、日時処理をするためのメソッドが提供されています。

## datetime


```
 from datetime import datetime, date
 
 date.today() + datetime.timedelta(hours30)   # 30時間後
 date.today() + datetime.timedelta(days=30)   # 30日後
 date.today() + datetime.timedelta(weeks=30)  # 50週後
 date.today() - datetime.timedelta(days=365)  $ 365日後
```

- [pandasでの日時処理]

## 指定した期間でフィルタリング


```
 df[(df["Date"] > "2018-01-01") & (df["Date"] < "2019-01-01")]
```


```
 In [2]: # %load c50_filter_by_date.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('stockdata.csv', parse_dates=["Date"])
    ...:
    ...: df1 = df[(df["Date"] > "2012-01-01") & (df["Date"] < "2013-06-01")]
    ...:
 
 In [3]: df1.info()
 <class 'pandas.core.frame.DataFrame'>
 Int64Index: 1770 entries, 6300 to 8069
 Data columns (total 5 columns):
  #   Column      Non-Null Count  Dtype
 ---  ------      --------------  -----
  0   Unnamed: 0  1770 non-null   int64
  1   Date        1770 non-null   datetime64[ns]
  2   stock       1770 non-null   object
  3   value       1770 non-null   float64
  4   change      1770 non-null   float64
 dtypes: datetime64[ns](1), float64(2), int64(1), object(1)
 memory usage: 83.0+ KB
 
 In [4]: df1
 Out[4]:
       Unnamed: 0       Date stock        value    change
 6300        6300 2012-01-03  MSFT    23.773104  2.353378
 6301        6301 2012-01-03   IBM   168.200853 -0.407950
 6302        6302 2012-01-03  SBUX    21.351952  1.943026
 6303        6303 2012-01-03  AAPL    54.405100  0.537415
 6304        6304 2012-01-03  GSPC  1277.060059  0.018792
 ...          ...        ...   ...          ...       ...
 8065        8065 2013-05-31  MSFT    32.358648  1.977073
 8066        8066 2013-05-31   IBM   192.675202  0.447069
 8067        8067 2013-05-31  SBUX    30.421491  0.506809
 8068        8068 2013-05-31  AAPL    60.776444  0.220128
 8069        8069 2013-05-31  GSPC  1630.739990  0.593599
 
 [1770 rows x 5 columns]
 
 In [5]:
 
```


## 指定した日/月/年でフィルタリング


```
 df[df["Date"].dt.strftime("%Y-%m-%d") == "2012-01-01"]
 df[df["Date"].dt.strftime("%m") == "12"]
 df[df["Date"].dt.strftime("%Y") == "2012"]
```


```
 In [2]: # %load c51_filter_by_pattern.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('stockdata.csv', parse_dates=["Date"])
    ...:
    ...: df1 = df[df["Date"].dt.strftime("%Y-%m-%d") == "2007-01-03"]
    ...: df2 = df[df["Date"].dt.strftime("%m") == "12"]
    ...: df3 = df[df["Date"].dt.strftime("%Y") == "2012"]
    ...:
 
 In [3]: df1
 Out[3]:
    Unnamed: 0       Date stock        value    change
 0           0 2007-01-03  MSFT    23.950705 -0.167452
 1           1 2007-01-03   IBM    80.517962  1.069189
 2           2 2007-01-03  SBUX    16.149666  0.113476
 3           3 2007-01-03  AAPL    11.086612  2.219569
 4           4 2007-01-03  GSPC  1416.599976  0.122829
 
 In [4]: df2
 Out[4]:
        Unnamed: 0       Date stock        value    change
 1155         1155 2007-12-03  MSFT    26.763891 -0.455644
 1156         1156 2007-12-03   IBM    88.835658  0.755925
 1157         1157 2007-12-03  SBUX    10.450322 -2.060492
 1158         1158 2007-12-03  AAPL    23.662904  0.531144
 1159         1159 2007-12-03  GSPC  1472.420044 -0.654026
 ...           ...        ...   ...          ...       ...
 11325       11325 2015-12-31  MSFT    55.084498 -1.225666
 11326       11326 2015-12-31   IBM   136.228490 -1.213485
 11327       11327 2015-12-31  SBUX    59.834461 -2.948527
 11328       11328 2015-12-31  AAPL   104.691918  0.085499
 11329       11329 2015-12-31  GSPC  2043.939941 -1.530373
 
 [960 rows x 5 columns]
 
 In [5]: df3
 Out[5]:
       Unnamed: 0       Date stock        value    change
 6300        6300 2012-01-03  MSFT    23.773104  2.353378
 6301        6301 2012-01-03   IBM   168.200853 -0.407950
 6302        6302 2012-01-03  SBUX    21.351952  1.943026
 6303        6303 2012-01-03  AAPL    54.405100  0.537415
 6304        6304 2012-01-03  GSPC  1277.060059  0.018792
 ...          ...        ...   ...          ...       ...
 7545        7545 2012-12-31  MSFT    24.390639  3.406971
 7546        7546 2012-12-31   IBM   175.852216  2.505875
 7547        7547 2012-12-31  SBUX    25.656212  2.554535
 7548        7548 2012-12-31  AAPL    71.030509  3.168158
 7549        7549 2012-12-31  GSPC  1426.189941  2.540342
 
 [1250 rows x 5 columns]
 
 In [6]:
 
```


# その他
## 列のデータの最小値と最大値の位置を取得する
 `idxmin()` と  `idxmax()` で最小値と最大値がある位置を取得することができます。また、 `iloc` にその結果を与えると、該当する行が取得することができます。


```
 df['col'].idxmin()
 df['col'].idxmax()
```


```
 In [2]: # %load c60_min_max.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('TSLA.csv', parse_dates=["Date"])
    ...:
    ...: v1 = df['Adj Close'].idxmin()
    ...: v2 = df['Adj Close'].idxmax()
    ...:
    ...: # df.iloc[v1]
    ...: # df.iloc[v2]
    ...:
 
 In [3]: v1
 Out[3]: 8
 
 In [4]: v2
 Out[4]: 2477
 
 In [5]: df.iloc[v1]
 Out[5]:
 Date         2012-01-13 00:00:00
 High                         5.7
 Low                        4.528
 Open                        5.68
 Close                      4.558
 Volume                27502000.0
 Adj Close                  4.558
 Name: 8, dtype: object
 
 In [6]: df.iloc[v2]
 Out[6]:
 Date         2021-11-04 00:00:00
 High                  1243.48999
 Low                       1217.0
 Open                 1234.410034
 Close                1229.910034
 Volume                25397400.0
 Adj Close            1229.910034
 Name: 2477, dtype: object
 
 In [7]: df.iloc[-1]
 Out[7]:
 Date         2022-05-16 00:00:00
 High                   769.76001
 Low                   719.088501
 Open                  767.159973
 Close                 724.369995
 Volume                28699513.0
 Adj Close             724.369995
 Name: 2609, dtype: object
 
 In [8]:
 
```


## データフレーム全体に関数を適用する


```
 df.applymao(func)
```


```
 In [2]: # %load c61_applymap.py
    ...: import pandas as pd
    ...: import numpy as np
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...: df1 = df.applymap(lambda x: 'True' if x == 'female' else 'False')
    ...:
 
 In [3]: df['sex']
 Out[3]:
 0        male
 1      female
 2      female
 3      female
 4        male
         ...
 886      male
 887    female
 888    female
 889      male
 890      male
 Name: sex, Length: 891, dtype: object
 
 In [4]: df1['sex']
 Out[4]:
 0      False
 1       True
 2       True
 3       True
 4      False
        ...
 886    False
 887     True
 888     True
 889    False
 890    False
 Name: sex, Length: 891, dtype: object
 
 In [5]:
 
```


## 変化率を取得する
 `pct_change()` を呼び出すと変化率を返してくれます。


```
 df['col'].pct_change()
```


```
 In [2]: # %load c62_percent_change.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('TSLA.csv', parse_dates=["Date"])
    ...: df['Change'] = df['Adj Close'].pct_change()
    ...:
 
 In [3]: df.info()
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 2610 entries, 0 to 2609
 Data columns (total 8 columns):
  #   Column     Non-Null Count  Dtype
 ---  ------     --------------  -----
  0   Date       2610 non-null   datetime64[ns]
  1   High       2610 non-null   float64
  2   Low        2610 non-null   float64
  3   Open       2610 non-null   float64
  4   Close      2610 non-null   float64
  5   Volume     2610 non-null   float64
  6   Adj Close  2610 non-null   float64
  7   Change     2609 non-null   float64
 dtypes: datetime64[ns](1), float64(7)
 memory usage: 163.2 KB
 
 In [4]: df[-5:-1]
 Out[4]:
            Date        High         Low  ...      Volume   Adj Close    Change
 2605 2022-05-10  825.359985  774.250000  ...  28133900.0  800.039978  0.016427
 2606 2022-05-11  809.770020  727.200012  ...  32408200.0  734.000000 -0.082546
 2607 2022-05-12  759.659973  680.000000  ...  46771000.0  728.000000 -0.008174
 2608 2022-05-13  787.349976  751.570007  ...  30651800.0  769.590027  0.057129
 
 [4 rows x 8 columns]
 
 In [3]: 728/734
 Out[3]: 0.9918256130790191
 
 In [4]: 1-728/734
 Out[4]: 0.008174386920980936
 
 In [5]:
 
```

## 出現データの頻度の10位を知る


```
 top_10 = df['col'].value_counts().nlargest(10).index
 df['col'].where(df['col'].isin(top_10), other="Other")
```


```
 In [2]: # %load c63_top10.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...:
    ...: fare_orig = df['fare']
    ...: top_10 = fare_orig.value_counts().nlargest(10).index
    ...: fare_new = fare_orig.where(fare_orig.isin(top_10), other="Other")
    ...: v1 = fare_new.value_counts()
    ...:
 
 In [3]: top_10
 Out[3]: Float64Index([8.05, 13.0, 7.8958, 7.75, 26.0, 10.5, 7.925, 7.775, 7.2292, 0.0], dtype='float64')
 
 In [4]: fare_new
 Out[4]:
 0      Other
 1      Other
 2      7.925
 3      Other
 4       8.05
        ...
 886     13.0
 887    Other
 888    Other
 889    Other
 890     7.75
 Name: fare, Length: 891, dtype: object
 
 In [5]: v1
 Out[5]:
 Other     615
 8.05       43
 13.0       42
 7.8958     38
 7.75       34
 26.0       31
 10.5       24
 7.925      18
 7.775      16
 7.2292     15
 0.0        15
 Name: fare, dtype: int64
 
 In [6]:
 
```


## グループ別に集計


```
 df.groupby(['sex', 'survived'])['survived'].sum()
```


```
 In [2]: # %load c64_groupby.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('titanic.csv')
    ...:
    ...: v1 = df.groupby(['sex', 'survived'])['survived'].sum()
    ...:
 
 In [3]: v1
 Out[3]:
 sex     survived
 female  0             0
         1           233
 male    0             0
         1           109
 Name: survived, dtype: int64
 
 In [4]:
 
```

## 列データの展開
 `explode()` はリストを展開してくれます。いくつかの行にデータのリストがあるときに便利です。


```
 In [2]: # %load c65_explode.py
    ...: import pandas as pd
    ...:
    ...: df = pd.DataFrame({"name": ['A', 'B', 'C'],
    ...:                    "day1": [21, 22, 23],
    ...:                    'day2':[31, 32, 33],
    ...:                    'day3': [41, 42, 43],
    ...:                    'day4': [51, 52, [53, 54, 55, 56, 57]],
    ...:                    'day5': [61, 61, 62]})
    ...:
    ...: v1 = df.explode('day4').reset_index(drop=True)
    ...:
 
 In [3]: df
 Out[3]:
   name  day1  day2  day3                  day4  day5
 0    A    21    31    41                    51    61
 1    B    22    32    42                    52    61
 2    C    23    33    43  [53, 54, 55, 56, 57]    62
 
 In [4]: v1
 Out[4]:
   name  day1  day2  day3 day4  day5
 0    A    21    31    41   51    61
 1    B    22    32    42   52    61
 2    C    23    33    43   53    62
 3    C    23    33    43   54    62
 4    C    23    33    43   55    62
 5    C    23    33    43   56    62
 6    C    23    33    43   57    62
 
 In [5]:
 
```


### 日足データから週足データをつくる
 `resample()` に  `"W"` を与えると時系列データを1週間単位でリサンプリングしてくれます。どうように  `"M"` で月単位となります。


```
 df.resample('W').agg(
     {'High': 'max', 'Low': 'min', 'Open': 'first', 
      'Close': 'last', 'Volume': 'sum', 'Adj Close': 'last' }
     
```


```
 In [2]: # %load c66_stock_weekly.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('TSLA.csv',
    ...:                  parse_dates=['Date'], index_col='Date')
    ...:
    ...: df_w = df.resample('W').agg(
    ...:                   {'High': 'max', 'Low': 'min', 'Open': 'first',
    ...:                   'Close': 'last', 'Volume': 'sum', 'Adj Close': 'last' })
    ...:
 
 In [3]: df.head()
 Out[3]:
              High    Low   Open  Close     Volume  Adj Close
 Date
 2012-01-03  5.900  5.530  5.788  5.616  4640500.0      5.616
 2012-01-04  5.734  5.500  5.642  5.542  3150500.0      5.542
 2012-01-05  5.586  5.370  5.552  5.424  5027500.0      5.424
 2012-01-06  5.558  5.282  5.440  5.382  4931500.0      5.382
 2012-01-09  5.498  5.224  5.400  5.450  4485000.0      5.450
 
 In [4]: df_w.head()
 Out[4]:
              High    Low   Open  Close      Volume  Adj Close
 Date
 2012-01-08  5.900  5.282  5.788  5.382  1.7750e+07      5.382
 2012-01-15  5.724  4.528  5.400  4.558  4.2354e+07      4.558
 2012-01-22  5.548  5.250  5.324  5.320  3.9102e+07      5.320
 2012-01-29  5.944  5.288  5.362  5.866  2.0416e+07      5.866
 2012-02-05  6.266  5.706  5.898  6.230  1.8894e+07      6.230
 
 In [5]:
 
```

## 指数平滑移動平均を求める
#### 指数平滑移動平均（EMA： Exponential Moving Average）


```
 df["EMA5"] = df["close"].ewm(span=5, adjust=False).mean()
 df["EMA25"] = df["close"].ewm(span=25, adjust=False).mean()
 df["EMA75"] = df["close"].ewm(span=75, adjust=False).mean()
```


## メモリ使用量を知る


```
 df.memory_usage()
 df.memory_usage().sum()
```


```
 In [2]: # %load c67_memory_usage.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('TSLA.csv', parse_dates=["Date"])
    ...: v1 = df.memory_usage()
    ...: v2 = df.memory_usage().sum()
    ...:
 
 In [3]: v1
 Out[3]:
 Index          128
 Date         20880
 High         20880
 Low          20880
 Open         20880
 Close        20880
 Volume       20880
 Adj Close    20880
 dtype: int64
 
 In [4]: v2
 Out[4]: 146288
 
 In [5]:
 
```

# スタイリング
## 書式指定 数値フォーマット

 `display.float_format` で書式を設定するとそれ以後は、指定した書式で出力されます。

```
 pd.set_option('display.float_format', lambda x: '%.3f' % x)     # 小数点以下3桁まで表示
 pd.options.display.float_format = '{:,.0f}'.format              # 財務表などのよういカンマ区切りで表示
```



```
 In [2]: # %load c70_format.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('TSLA.csv', parse_dates=['Date'])
    ...:
    ...: # df
    ...: # pd.set_option('display.float_format', lambda x: '%.3f' % x)
    ...: # df
    ...: # pd.options.display.float_format = '{:,.0f}'.format
    ...: # df
    ...:
 
 In [3]: df
 Out[3]:
            Date        High         Low  ...       Close      Volume   Adj Close
 0    2012-01-03    5.900000    5.530000  ...    5.616000   4640500.0    5.616000
 1    2012-01-04    5.734000    5.500000  ...    5.542000   3150500.0    5.542000
 2    2012-01-05    5.586000    5.370000  ...    5.424000   5027500.0    5.424000
 3    2012-01-06    5.558000    5.282000  ...    5.382000   4931500.0    5.382000
 4    2012-01-09    5.498000    5.224000  ...    5.450000   4485000.0    5.450000
 ...         ...         ...         ...  ...         ...         ...         ...
 2605 2022-05-10  825.359985  774.250000  ...  800.039978  28133900.0  800.039978
 2606 2022-05-11  809.770020  727.200012  ...  734.000000  32408200.0  734.000000
 2607 2022-05-12  759.659973  680.000000  ...  728.000000  46771000.0  728.000000
 2608 2022-05-13  787.349976  751.570007  ...  769.590027  30651800.0  769.590027
 2609 2022-05-16  769.760010  719.088501  ...  724.369995  28699513.0  724.369995
 
 [2610 rows x 7 columns]
 
 In [4]: pd.set_option('display.float_format', lambda x: '%.3f' % x)
 
 In [5]: df
 Out[5]:
            Date    High     Low    Open   Close       Volume  Adj Close
 0    2012-01-03   5.900   5.530   5.788   5.616  4640500.000      5.616
 1    2012-01-04   5.734   5.500   5.642   5.542  3150500.000      5.542
 2    2012-01-05   5.586   5.370   5.552   5.424  5027500.000      5.424
 3    2012-01-06   5.558   5.282   5.440   5.382  4931500.000      5.382
 4    2012-01-09   5.498   5.224   5.400   5.450  4485000.000      5.450
 ...         ...     ...     ...     ...     ...          ...        ...
 2605 2022-05-10 825.360 774.250 819.310 800.040 28133900.000    800.040
 2606 2022-05-11 809.770 727.200 795.000 734.000 32408200.000    734.000
 2607 2022-05-12 759.660 680.000 701.000 728.000 46771000.000    728.000
 2608 2022-05-13 787.350 751.570 773.480 769.590 30651800.000    769.590
 2609 2022-05-16 769.760 719.089 767.160 724.370 28699513.000    724.370
 
 [2610 rows x 7 columns]
 
 In [6]: pd.options.display.float_format = '{:,.0f}'.format
 
 In [7]: df
 Out[7]:
            Date  High  Low  Open  Close     Volume  Adj Close
 0    2012-01-03     6    6     6      6  4,640,500          6
 1    2012-01-04     6    6     6      6  3,150,500          6
 2    2012-01-05     6    5     6      5  5,027,500          5
 3    2012-01-06     6    5     5      5  4,931,500          5
 4    2012-01-09     5    5     5      5  4,485,000          5
 ...         ...   ...  ...   ...    ...        ...        ...
 2605 2022-05-10   825  774   819    800 28,133,900        800
 2606 2022-05-11   810  727   795    734 32,408,200        734
 2607 2022-05-12   760  680   701    728 46,771,000        728
 2608 2022-05-13   787  752   773    770 30,651,800        770
 2609 2022-05-16   770  719   767    724 28,699,513        724
 
 [2610 rows x 7 columns]
 
 In [8]:
 
```


## 書式指定  Jupyter環境
Pandas を Jupyterlab/notebok から使用している場合は、書式を指定することができます。


```
 import pandas as pd
 
 df = pd.read_csv('TSLA.csv', parse_dates=["Date"])
 
 format_dict = {
     "Date": "{:%d/%m/%y}",
     "Open": "${:.2f}",
     "High": "${:.2f}",
     "Low": "${:.2f}",
     "Close": "${:.2f}",
     "Ajd Close": "${:.2f}",
     "Volume": "{:,}",
 }
 
 df.style.format(format_dict)
```

![](https://gyazo.com/4756174db0f7fec7a9cb25e3a4ae8fe1.png)

## カラー指定
Pandas を Jupyterlab/notebok から使用している場合は、色を指定することもできます。


```
 (
     df.style.format(format_dict)
     .highlight_min(["Open"], color="red")
     .highlight_max(["Open"], color="green")
     .background_gradient(subset="Close", cmap="Greens")
     .bar('Volume', color='lightblue', align='zero')
     .set_caption('Tesla Stock Prices in 2018')
     .hide()
 )
 
```

![](https://gyazo.com/b5c182bb902f2f26f99e66712702a599.png)

## おまけ
次のようなファイルを  `.pythonrc.py` もしくは  `~/.ipython/profile_default/startup/00_startup.py` におけば
毎回起動時にPandas の設定を行ってくれて便利になります。オプションの値は適宜お望みの設定に変更してください。


 pandas_config.py
```
 import pandas as pd
 
 def start():
 
     def dict_merge(a, b):
         for key in b:
             if isinstance(a.get(key), dict) or isinstance(b.get(key), dict):
                 dict_merge(a[key], b[key])
             else:
                 a[key] = b[key]
         return a
 
     default_options ={
         'display': {
             'max_columns': None,
             'max_colwidth': 25,
             'expand_frame_repr': False,
             'max_rows': 14,
             'max_seq_items': 50,
             'precision': 4,
             'show_dimensions': False,
         },
         'mode': {
             'chained_assignment': None
         }
     }
 
     import sys,os
     sys.path.append(os.getcwd())
     try:
         from pandas_config import options
         options = dict_merge(default_options, options)
     except:
         pass
     options = default_options
     for category, option in options.items():
         for op, value in option.items():
             pd.set_option(f'{category}.{op}', value)
 
 if __name__ == '__main__':
     import os
     flag = os.environ.get('PANDAS_SKIP_STARTUP', default=None)
     _ = not flag and start()
     del start
     del flag
         
```

環境変数で  `export PANDAS_SKIP_STARTUP=1` などのようにしてから起動すると、この処理をスキップされます。 `PYTHON_PATH` で設定されているパスか、カレントディレクトリに  `pandas_config.py` があれば、そこから辞書  `options` をインポートしてデフォルト設定を上書きします。プロジェクトごとに pandas の設定を変えたいようなときに使えます。 
例えば、 `pandas_config.py` を以下のように記述すると、小数点以下3桁の書式となります。

 pandas_config.py
```
 options = {
     'display': {
         'float_format': lambda x: '%.3f' % x,
     },
 }
 
```

# 参考
- Pandas
  - [Pandas オフィシャルサイト https://pandas.pydata.org/
  - [Pandas 公式ドキュメント ](https://pandas.pydata.org/pandas-docs/stable/index.html)
  - [Pandas Cheat Sheet (Official) ](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)


