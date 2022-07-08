Pandasでのデータ入出力
=================
### データの読み込み

Pandas は次のフォーマット形式のデータを読み書きすることができます。
 Pandas データIO

| Format Type | Data Description | Reader | Writer |
|:--|:--|:--|:--|
| text | CSV | read_csv | to_csv |
| text | Fixed-Width Text File | read_fwf     | N/A |
| text | JSON | read_json | to_json |
| text | HTML | read_html | to_html |
| text | Local clipboard | read_clipboard | to_clipboard |
| binary | MS Excel | read_excel | to_excel |
| binary | OpenDocument | read_excel | N/A |
| binary | HDF5 Format | read_hdf | to_hdf |
| binary | Feather Format | read_feather | to_feather |
| binary | Parquet Format | read_parquet | to_parquet |
| binary | ORC Format | read_orc | N/A |
| binary | Msgpack | read_msgpack | to_msgpack |
| binary | Stata | read_stata |  to_stata |
| binary | SAS | read_sas | N/A |
| binary | SPSS | read_spss | N/A |
| binary | Python Pickle Format | read_pickle | to_pickle |
| SQL | SQL | read_sql | to_sql |
| SQL | Google BigQuery | read_gbq | to_gbq |

#### CSVファイルからの読み込み
 IPython
```
 import pandas as pd
 df = pd.read_csv('sample.csv')
```

#### JSONファイルからの読み込み
 IPython
```
 import pandas as pd
 df = pd.read_json('sample.json')
```

#### EXCELファイルからの読み込み

```
 import pandas as pd
 df = pd.read_excel('sample.xlsx')
 # シートを指定して読み込み　シート番号もしくはシート名を当てる
 df_sheet_index = pd.read_excel('sample.xlsx', sheet_name='Sheet 1')
```
　
- # 複数のシートを指定して読み込み シート番号はゼロはじまり
- df_sheet_multi = pd.read_excel('sample.xlsx', sheet_name=[0, 'sheet2'])
 
- # すべてのシートを読み込み
- df_sheet_all = pd.read_excel('sample.xlsx', sheet_name=None)


xlrd モジュールがインストールされていないと、次のようなエラーが表示されます。
> ImportError: Install xlrd >= 0.9.0 for Excel support

この場合は、pip でインストールします。
 zsh
```
 % pip install xlrd
```

#### SQLでデータベースから読み込む
 IPython
```
 import pandas as pd
 import sqlite3
 conn = sqlite3.connect("sample.db")
 df = pd.read_sql_query("SELECT * FROM sample", conn)
```

### データの書き込み
読み込んだデータをデータフレームオブジェクトを介して別のフォーマットに書き込むこともできます。

#### CSVファイルとして出力
 IPython
```
 import pandas as pd
 # ...
 df = pd.to_csv('sample.csv')
```

#### JSONファイルとして出力
 IPython
```
 import pandas as pd
 # ...
 df.to_json('sample.json')
```

#### EXCELファイルとして出力
 IPython
```
 import pandas as pd
 # ...
 df.to_excel('sample.xls')
 
 # シートを指定して出力　シート番号もしくはシート名を当てる
  df_sheet_index = pd.read_excel('sample.xlsx', sheet_name='Sheet 1')
  
 # 既存のEXCELファイルに追加
 with pd.ExcelWriter('sample.xlsx', 'a') as writer:
     df.to_excel(writer, sheet_name='Sheet_name_3')
 
 # EXCELファイルを書き出すエンジンを指定する
 df = pd.to_excel('sample1.xlsx', engine='xlsxwriter')
```

xlwt モジュールがインストールされていないと、次のようなエラーが表示されます。
>ModuleNotFoundError: No module named 'xlwt'

この場合は、pip でインストールします。
 zsh
```
 % pip install xlwt
```

 `to_excel()` メソッドは次のモジュールに依存しています。
- **xlwt**：拡張子が  `.xls` のEXCELファイル(Excel2003以前)
- **openpyxl**： 拡張子が  `.xlsx` のEXCELファイル (Excel2007以降)

#### データベースへ出力
 IPython
```
 import pandas as pd
 import sqlite3
 # ...
 conn = sqlite3.connect("example.db")
 df.to_sql("example", conn)
```

引数に  `if_exists` を与えることで、テーブルが存在するときの挙動を指定することができます。

-  `if_exists = 'fail'` ：テーブルが存在する場合は  `ValueError` が発生（デフォルト）
-  `if_exists = 'replace'` ：テーブルを削除し、新しい値をインサート
-  `if_exists = 'append'` ：テーブルに新しい値を追加します。

#### HTMLで出力
 IPython
```
 In [2]: # %load pandas_html_write.py 
    ...: import numpy as np 
    ...: import pandas as pd 
    ...:  
    ...: df = pd.DataFrame(np.random.randn(2, 2)) 
    ...: print(df.head()) 
    ...: print(df.to_html()) 
    ...:                                                                           
           0         1
 0  1.025031  0.090243
 1 -0.542508  0.885818
 <table border="1" class="dataframe">
   <thead>
     <tr style="text-align: right;">
       <th></th>
       <th>0</th>
       <th>1</th>
     </tr>
   </thead>
   <tbody>
     <tr>
       <th>0</th>
       <td>1.025031</td>
       <td>0.090243</td>
     </tr>
     <tr>
       <th>1</th>
       <td>-0.542508</td>
       <td>0.885818</td>
     </tr>
   </tbody>
 </table>
```

### その他のデータ入出力
### URLを指定してCSVファイルを読み込み
拡張モジュール html5lib がインストールされていれば、URLを指定してCSVファイルを読み込むことができます。
 IPython
```
 In [2]: # %load pandas_csv_readfromurl.py 
    ...: import pandas as pd 
    ...:  
    ...: baseurl = 'https://github.com/pandas-dev/pandas/raw/master/pandas' 
    ...: url = baseurl + '/tests/data/iris.csv' 
    ...: df = pd.read_csv(url) 
    ...:                                                                           
 
 In [3]: df.head()                                                          Out[3]: 
    SepalLength  SepalWidth  PetalLength  PetalWidth         Name
 0          5.1         3.5          1.4         0.2  Iris-setosa
 1          4.9         3.0          1.4         0.2  Iris-setosa
 2          4.7         3.2          1.3         0.2  Iris-setosa
 3          4.6         3.1          1.5         0.2  Iris-setosa
 4          5.0         3.6          1.4         0.2  Iris-setosa
```

### インストール
html5lib  は拡張モジュールなので次のようにインストールします。
 bash condaの場合
```
 $ conda install htmll5lib
 bash pipの場合
```
 $ pip install html5lib
```

### URLを指定してCSVファイルを読み込み: その２
前述の方法では、サイト側で「非ブラウザ」からのリクエストを許可しない設定になっている場合は、次のようなエラーになってしまいます。

```
 ~/anaconda3/envs/py36/lib/python3.6/urllib/request.py in http_error_default(self, req, fp, code, msg, hdrs)
     648 class HTTPDefaultErrorHandler(BaseHandler):
     649     def http_error_default(self, req, fp, code, msg, hdrs):
 --> 650         raise HTTPError(req.full_url, code, msg, hdrs, fp)
     651 
     652 class HTTPRedirectHandler(BaseHandler):
 
 HTTPError: HTTP Error 403: Forbidden
```

この場合は、次のように拡張モジュール requests を使って処理をするとうまくいきます。
 IPython
```
 In [2]: # %load pandas_csv_readfromurl2.py 
    ...: import io 
    ...: import requests 
    ...: import pandas as pd 
    ...:  
    ...: baseurl = 'https://www.analyticsvidhya.com/wp-content/uploads' 
    ...: url = baseurl + '/2016/02/AirPassengers.csv' 
    ...:  
    ...: raw_data = requests.get(url).content 
    ...: df = pd.read_csv(io.StringIO(raw_data.decode('utf-8'))) 
    ...:                                                                           
 In [3]: df.head()                                                          Out[3]: 
      Month  #Passengers
 0  1949-01          112
 1  1949-02          118
 2  1949-03          132
 3  1949-04          129
 4  1949-05          121
```


### マークダウン
拡張モジュール tabulate がインストールされていれば、データフレームからマークダウン形式で書き出すことができます。

 pandas_markdown_write.py 
```
 import numpy as np
 import pandas as pd
 
 df = pd.DataFrame(np.random.randn(2, 2))
 print(df.head())
 print(df.to_markdown())
```


 IPyhon
```
 In [2]: # %load pandas_markdown_write.py 
    ...: import numpy as np 
    ...: import pandas as pd 
    ...:  
    ...: df = pd.DataFrame(np.random.randn(2, 2)) 
    ...: print(df.head()) 
    ...: print(df.to_markdown()) 
    ...:  
    ...: with open('./sample.md', 'w') as f: 
    ...:     df.describe().to_markdown(f) 
    ...:                                                                           
           0         1
 0 -0.260100  1.679956
 1 -0.478981 -0.730784
 |    |         0 |         1 |
 |---:|----------:|----------:|
 |  0 | -0.2601   |  1.67996  |
 |  1 | -0.478981 | -0.730784 |
 
 In [3]: !cat sample.md                                                            
 |       |         0 |         1 |
 |:------|----------:|----------:|
 | count |  2        |  2        |
 | mean  | -0.36954  |  0.474586 |
 | std   |  0.154772 |  1.70465  |
 | min   | -0.478981 | -0.730784 |
 | 25%   | -0.424261 | -0.128099 |
 | 50%   | -0.36954  |  0.474586 |
 | 75%   | -0.31482  |  1.07727  |
 | max   | -0.2601   |  1.67996  |
```

ファイルオブジェクトを引数として渡すとファイルにマークダウン形式で書き出すこともできます。

参考:
- [Python チュートリアル：データのテーブル出力]

### Pickleファイル
Python のPickleファイルは、Pythonオブジェクトのデータと階層を保持しているバイナリファイルです。 通常、拡張子は `.pickle` または `.pkl` が使用されます。Picklingは、Pythonオブジェクトをバイトストリームに変換する行為です。 UnPickling はピクリング解除するための逆手順です。


```
 import pandas as pd
 # ...
 original_df = pd.DataFrame({"foo": range(5), "bar": range(5, 10)})
 original_df.to_pickle('data.pickle')
 df = pd.read_pickle('data.pickle') 
```

### Pandas で Webスクレイピング
Pandasを使用すると、Webページのテーブル（ `<table>` タグ）を簡単にスクレイピングすることができます。 DataFrameとして取得したあと、さまざまなデータ処理を行って、Excel、CSV、JSONなどの形式でファイルとして保存することもできます。

Pandas で Webスクレイピングを行う場合は、次の依存モジュールをインストールします。
 zsh
```
 % pip install lxml html5lib beautifulsoup4
```

#### URLを指定したHTMLを読み込む
 `<table>` タグが読み込まれデータフレームが返されます。
複数の `<table>` タグがあるときは、データフレームのリストが返されます。
 IPython
```
 In [2]: # %load pandas_html_read.py 
    ...: import pandas as pd 
    ...:  
    ...: url = 'https://www.fdic.gov/bank/individual/failed/banklist.html' 
    ...: data = pd.read_html(url) 
    ...: print(type(data)) 
    ...: print(data) 
    ...:  
    ...:                                                                           
 <class 'list'>
 [                             Bank Name  ...       Closing Date
 0                 The First State Bank  ...      April 3, 2020
 1                   Ericson State Bank  ...  February 14, 2020
 2     City National Bank of New Jersey  ...   November 1, 2019
 3                        Resolute Bank  ...   October 25, 2019
 4                Louisa Community Bank  ...   October 25, 2019
 ..                                 ...  ...                ...
 556                 Superior Bank, FSB  ...      July 27, 2001
 557                Malta National Bank  ...        May 3, 2001
 558    First Alliance Bank & Trust Co.  ...   February 2, 2001
 559  National State Bank of Metropolis  ...  December 14, 2000
 560                   Bank of Honolulu  ...   October 13, 2000
 
 [561 rows x 6 columns]]
```

## CSVフォーマットの長所と短所
すべての技術的な仕様と同様に、CSVフォーマットでデータを保存することには長所と短所の両方があります。 CSV形式でデータをロード、保存、交換するときに、問題が発生する可能性があることを意識する必要があります。

### 長所
- CSV形式は普遍的であり、データはほとんどすべてのソフトウェアでロードできる
- CSVファイルは、基本的なテキストエディタを使用して簡単に理解およびデバッグできる
- CSVファイルは、分析前にすばやく作成してメモリにロードできる

### 短所
- テキストファイルにはデータ型情報は保存されない
  - すべてのデータは（日付、intとfloat、文字列）はデータからのみ推測される
- 保存可能なフォーマットやレイアウト情報がない
  - フォント、境界線、MicrosoftExcelの列幅設定などは失われる
- テキストにASCII非互換の文字があれば、エンコーディングが問題になることがある
- CSV形式は非効率的なこと
  - 数値がバイナリではなく文字として格納されるため、ファイルサイズが大きくなる
  - ただし、CSVデータはzip圧縮を使用して圧縮することができる

> 余談
> 単純で高速に複数のデータ型をネィティブのサポートする、
> オープンソースでマルチプラットフォームの[feather ](https://github.com/wesm/feather)フォーマットが提唱されています。


### CSVファイルで想定されるエラー
Pandas で外部ファイルからデータを読み込むときに発生する一般的なエラーは次のとおりです。

-  `FileNotFoundError` ：指定したファイル存在しません
 `File Not Found` エラーは通常、パスの設定、現在のディレクトリ、またはファイル名に誤りがある場合に発生します。ファイル拡張子に誤りがあるか、指定されていない場合もありますｌ．
 `UnicodeDecodeError` ：  `'utf-8'` コーデックはバイトを所定の位置でデコードできません `UnicodeDecodeError` は通常、ファイルのエンコーディングを指定しない場合に発生します。非標準文字を含むファイルがある場合にも発生します。 簡単に修正するには、アプリケーション [Sublime Text ](https://www.sublimetext.com/3) でファイルを開き、エンコーディング `UTF-8` を指定して再保存してみてください。
-  `pandas.parser.CParserError` ：データのトークン化中にエラーが発生しました。
解析エラーは、データ形式に関係する異常な状況で発生することがあります。この場合、関数  `read_csv()` に 引数  `engine=’python'` を与えることで、データ読み取り機能が内部的により安定した方法に変更されます。読み込み速度は低下します。

### データ・タイプを指定したCSVファイルの読み込み
CSVファイルにはデータの型情報は含まれていません。 データ型は、ファイルの一番上の行を調べることで推測することができますが、エラーが発生する可能性があります。 Pandas では、 `read_csv()` でCSVファイルを読み込むときに、さまざまな列のデータ型を読み込み時に指定することができます。


```
```
- read_csv('sample.csv', dtype = {"name"：str、 "age"：np.int32})

日付や日時の場合、形式、列、およびその他の動作は、 `parse_dates` 、 `date_parser` 、 `dayfirst` 、 `keep_date` パラメーターを使用して調整できる。

### CSVファイルから行と列のスキップと選択
関数  `read_csv()` に次の引数を与えることで、行と列の指定したり、スキップすることができます。
-  `nrows` ：CSVファイルの先頭から読み取る行数を指定
CSVファイルのサイズが大きいときに部分的に読み込むときに便利です
-  `skiprows` ：ファイルの先頭からの行数（int値を指定）や、ファイル全体から行インデックスのリストを指定することで除外する行を指定
-  `usecols` ：データ内のどの列を読み込むかを指定

### 欠落記号を変更
異なるシステムからCSVにデータをエクスポートする場合、  `na_values` 引数を使用することで、欠落データとして表現される文字をカスタマイズすることができます。
 `NA` /  `NaN` として解釈されるデフォルト値は次のものです。
‘#N/A’、‘#N/A N/A’、‘#NA’、‘-1.#IND’、‘-1.#QNAN’、‘-NaN’、‘-nan’、‘1.#IND’、‘1.#QNAN’、‘N/A’、‘NA’、‘NULL’、‘NaN’、‘n/a’、‘nan’、‘null’


```
 import pandas as pd
 data = pd.read_csv(
     "data/files/sample.tsv", 
     sep='\t'                # 区切り文字をタブに指定
     quotechar="'",          # 引用符にシングルクォートを指定
     dtype={"salary": int},  # salaryカラムを整数に変換 
     usecols=['name', 'birth_date', 'salary'].   # 読み込むカラムを指定
     parse_dates=['birth_date'],  # birth_dateカラムを日付に変換
     skiprows=10,            # 最初の10行をスキップ
     na_values=['.', '??']   # '.' もしくは '??' を欠落データ(NA)として読み込む
 )
```

previous: [Pandasの基本操作]
next: [pandas-datareaderを使ってみよう]
#Pythonセミナーデータ分析編

