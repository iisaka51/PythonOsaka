Excelファイルの読み書きしてみよう
=================
## はじめに
Python でExcelファイルを扱うためには、用途によって次のライブラリを使用することができます。

#### Excelファイル格納されているデータをPythonで分析したい
  - サポートしているファイル拡張子は　 `.xls` ,  `.xlsx` ,  `.xlsm` ,  `.xlsb` ,  `.odf` ,  `.ods` ,   `.odt` 
  - ExcelのデータとDataFrameオブジェクトの変換は  `read_excel()` と  `.to_excel()` 
  - Excelファイルをデータリソースとして読み書きできる
  - データ分析を行うことに目的があるとき
#### 既存のExcelファイルへPythonで編集/追記をしたい
  - サポートしているファイル拡張子は　 `.xlsx` ,  `.xlsm` ,  `.xltx` ,  `.xltm` 　(Office 2007移行のファイル)
  - 特定のセルだけを読み書きしたいときに便利
  - セルのフォーマットや色、フォントも扱える
  - チャートやイメージをワークシートに描画/追加ができる
#### Office 2007より前のExcelを読み書きしたい
  - xlrd - Excelファイル（ `.xls` ,  `.xlsx` ）の読み込みができる
  - xlwt - Excelファイル（ `.xls` ）の書き込みができる
#### OpenOffice のスプレッドシートを読み書きしたい
  - odf - Open Office のファイル( `.odf` ,  `.ods` ,  `.odt` )をサポート
#### Excel Binary Woklbookファイルを読み込みたい
  - pyxlsb - Excel Binary Workbookファイル( `xlsb` ) の読み込みができる
#### Excel の数式を Python で処理したい
  - xlcalculator - Excel の数式を Excel に依存せずに Python で処理できる
  - pycel - Excel の数式を Excel に依存せずに Python で処理できる
#### Excel のマクロを処理させたい
  - xlwings - Excelを実行させることでマクロをサポートしている。

サンプルのデータとして次のようなExcelファイル  `test.xlsx` があるとして説明することにします。
（[テスラ ](https://finance.yahoo.com/quote/TSLA?p=TSLA&.tsrc=fin-srch) の2015年からの株価日足データです）

![](https://gyazo.com/d8c9c1ac78f5c15b5591bce93a5e6371.png)


#### Excelファイルのフォーマット
Office 2007 から Open XMLフォーマットが採用されています。そのExcel ファイルは拡張子が  `.xslx` です 。このファイルの実態はZIPで圧縮されたXMLLファイルの集まりとなっています。

 bash
```
 $ unzip -l  test.xlsx
 Archive:  test.xlsx
   Length      Date    Time    Name
 ---------  ---------- -----   ----
      1168  01-01-1980 00:00   [Content_Types].xml
       588  01-01-1980 00:00   _rels/.rels
       698  01-01-1980 00:00   xl/_rels/workbook.xml.rels
      1463  01-01-1980 00:00   xl/workbook.xml
      2745  01-01-1980 00:00   xl/styles.xml
      6784  01-01-1980 00:00   xl/theme/theme1.xml
      2759  01-01-1980 00:00   xl/worksheets/sheet1.xml
       320  01-01-1980 00:00   xl/sharedStrings.xml
       593  01-01-1980 00:00   docProps/core.xml
       795  01-01-1980 00:00   docProps/app.xml
 ---------                     -------
     17913                     10 files
     
```


## Pandas でExcelファイルを扱う
Pandasはデータ分析のためのライブラリでExcelファイルをデータソースとして利用できるよう、Excelファイルの読み書きをサポートしています。はじめに紹介したライブラリを内部で使用しているため個々のライブラリの違いを吸収してくれます。読み出したデータは DataFrame というデータ形式で保持されます。このDataFrame ではデータの抽出/連結/加工/集計などが非常に簡単になるので、一番おすすめする方法です。

### インストール
pandas は pip コマンドでインストールすることができます。

 bash
```
 $ pip install pandas
```

### Excelファイルの読み込み
pandas で  `read_excel()` を呼び出すと指定したExcelファイルを読み込んでDataFrameオブジェクトを返します。


```
 In [2]: # %load c01_using_pandas.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_excel('test.xlsx', index_col=0)
    ...:
    ...: # print(df)
    ...: # print(df.head())
    ...: # print(df.tail())
    ...:
 
 In [3]: print(df)
                   High         Low  ...    Volume   Adj Close
 Date                                ...
 2015-01-02   44.650002   42.652000  ...  23822000   43.862000
 2015-01-05   43.299999   41.431999  ...  26842500   42.018002
 2015-01-06   42.840000   40.841999  ...  31309500   42.256001
 2015-01-07   42.956001   41.956001  ...  14842000   42.189999
 2015-01-08   42.759998   42.001999  ...  17212500   42.124001
 ...                ...         ...  ...       ...         ...
 2022-03-02  886.479980  844.270020  ...  24881100  879.890015
 2022-03-03  886.440002  832.599976  ...  20541200  839.289978
 2022-03-04  855.650024  825.159973  ...  22333200  838.289978
 2022-03-07  866.140015  804.570007  ...  24073300  804.580017
 2022-03-08  849.989990  782.169983  ...  26487200  824.400024
 
 [1808 rows x 6 columns]
 
 In [4]: print(df.head())
                  High        Low       Open      Close    Volume  Adj Close
 Date
 2015-01-02  44.650002  42.652000  44.574001  43.862000  23822000  43.862000
 2015-01-05  43.299999  41.431999  42.910000  42.018002  26842500  42.018002
 2015-01-06  42.840000  40.841999  42.012001  42.256001  31309500  42.256001
 2015-01-07  42.956001  41.956001  42.669998  42.189999  14842000  42.189999
 2015-01-08  42.759998  42.001999  42.562000  42.124001  17212500  42.124001
 
 In [5]: print(df.tail())
                   High         Low  ...    Volume   Adj Close
 Date                                ...
 2022-03-02  886.479980  844.270020  ...  24881100  879.890015
 2022-03-03  886.440002  832.599976  ...  20541200  839.289978
 2022-03-04  855.650024  825.159973  ...  22333200  838.289978
 2022-03-07  866.140015  804.570007  ...  24073300  804.580017
 2022-03-08  849.989990  782.169983  ...  26487200  824.400024
 
 [5 rows x 6 columns]
 
 In [6]:
```

### データの抽出
カラム  `Adj Close` の値が100ドル以下のデータを抜き出すといった場合でもDataFrameオブジェクトであれば簡単です。


```
 In [2]: # %load c02_pandas_extraction.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_excel('test.xlsx', index_col=0)
    ...:
    ...: newdf = df[df['Adj Close']<100]
    ...:
    ...: # print(newdf)
    ...:
 
 In [3]: print(newdf)
                   High        Low  ...     Volume  Adj Close
 Date                               ...
 2015-01-02   44.650002  42.652000  ...   23822000  43.862000
 2015-01-05   43.299999  41.431999  ...   26842500  42.018002
 2015-01-06   42.840000  40.841999  ...   31309500  42.256001
 2015-01-07   42.956001  41.956001  ...   14842000  42.189999
 2015-01-08   42.759998  42.001999  ...   17212500  42.124001
 ...                ...        ...  ...        ...        ...
 2020-03-20   95.400002  85.157997  ...  141427500  85.505997
 2020-03-23   88.400002  82.099998  ...   82272500  86.858002
 2020-04-01  102.790001  95.019997  ...   66766000  96.311996
 2020-04-02   98.851997  89.279999  ...   99292000  90.893997
 2020-04-03  103.098000  93.678001  ...  112810500  96.001999
 
 [1274 rows x 6 columns]
 
 In [4]:
```

(2年で株価が8.5倍になっていますね...)

### Excelファイルの書き出し
Excelファイルとして書き出すためには、DataFrameオブジェクトの  `to_excel()` メソッドを呼び出します。


```
 In [2]: # %load c03_pandas_writeexcel.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_excel('test.xlsx', index_col=0)
    ...:
    ...: newdf = df[df['Adj Close']<100]
    ...: newdf.to_excel('output.xlsx')
    ...:
    ...: df2 = pd.read_excel('output.xlsx', index_col=0)
    ...:
    ...: # print(newdf)
    ...: # print(df2)
    ...:
 
 In [3]: print(newdf)
                   High        Low  ...     Volume  Adj Close
 Date                               ...
 2015-01-02   44.650002  42.652000  ...   23822000  43.862000
 2015-01-05   43.299999  41.431999  ...   26842500  42.018002
 2015-01-06   42.840000  40.841999  ...   31309500  42.256001
 2015-01-07   42.956001  41.956001  ...   14842000  42.189999
 2015-01-08   42.759998  42.001999  ...   17212500  42.124001
 ...                ...        ...  ...        ...        ...
 2020-03-20   95.400002  85.157997  ...  141427500  85.505997
 2020-03-23   88.400002  82.099998  ...   82272500  86.858002
 2020-04-01  102.790001  95.019997  ...   66766000  96.311996
 2020-04-02   98.851997  89.279999  ...   99292000  90.893997
 2020-04-03  103.098000  93.678001  ...  112810500  96.001999
 
 [1274 rows x 6 columns]
 
 In [4]: print(df2)
                   High        Low  ...     Volume  Adj Close
 Date                               ...
 2015-01-02   44.650002  42.652000  ...   23822000  43.862000
 2015-01-05   43.299999  41.431999  ...   26842500  42.018002
 2015-01-06   42.840000  40.841999  ...   31309500  42.256001
 2015-01-07   42.956001  41.956001  ...   14842000  42.189999
 2015-01-08   42.759998  42.001999  ...   17212500  42.124001
 ...                ...        ...  ...        ...        ...
 2020-03-20   95.400002  85.157997  ...  141427500  85.505997
 2020-03-23   88.400002  82.099998  ...   82272500  86.858002
 2020-04-01  102.790001  95.019997  ...   66766000  96.311996
 2020-04-02   98.851997  89.279999  ...   99292000  90.893997
 2020-04-03  103.098000  93.678001  ...  112810500  96.001999
 
 [1274 rows x 6 columns]
 
 In [5]:
```


データ操作についてはPandas の知識が必要になりますが、それを理解していれば非常に簡単にデータ処理を行うことができます。

これは余談ですが、matplotlib モジュールがインストールされていれば、DataFrameオブジェクトの `plot()` メソッドを呼び出すだけでグラフ化することができます。


```
 In [2]: # %load c04_pandas_plot.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_excel('test.xlsx', index_col=0)
    ...:
    ...: # print(df['Adj Close'])
    ...:
    ...: # %matplotlib
    ...: # df['Adj Close'].plot()
    ...:
 
 In [3]: %matplotlib
 Using matplotlib backend: MacOSX
 
 In [4]: df['Adj Close'].plot()
 Out[4]: <AxesSubplot:xlabel='Date'>
 
 In [5]:
```

![](https://gyazo.com/178c16342d413d1283d51f46901dc3f5.png)
実は、このチュートリアルで使用している  `test.xlsx` も、次の pandas を利用したスクリプトで作成したものです。

 pandas_getstaock.py
```
 import datetime as dt
 import pandas as pd
 import pandas_datareader.data as web
 
 start = dt.datetime(2015, 1, 3)
 end = dt.datetime.now()
 df = web.DataReader("TSLA", 'yahoo', start, end)
 df.reset_index(inplace=True)
 # print(df.head())
 df.set_index("Date", inplace=True)
 df.to_excel('test.xlsx')
 
```

Pandas はデータソースとしてExcelだけでなく、CSV、JSON、SQL(データベース）、HDFなども扱うことができるなど、
非常に豊富な機能があるので、「[Pythonセミナーデータ分析編]」の第３章も参考にしてみてください。


## OpenPyXL でExcelファイルを扱う

![](https://gyazo.com/1844a333bb3a96a0ca764775f5d56cfa.png)
openpyxl は、Excel ファイルを読み書きするための Python ライブラリです。サポートしている拡張子は、 `.xlsx` ,   `.xlsx` ,  `.xlsm` ,  `.xltx` ,  `.xltm` です。Office Open XML形式のファイルをPythonからネイティブに読み書きするライブラリが存在しないことから生まれたものです。
OpenPyXL は Python でExcelファイルを作成/編集を行うことが目的としているライブラリです。

OpenPyXL ではExcelファイルにアクセスするときに次のコンポーネントを意識する必要があります。

 OpenPyXLのコンポーネント

| コンポーネント | 説明 | 例 |
|:--|:--|:--|
| Workbook | 作成または作業中のオブジェクトあるいはファイルです。 |  |
| Worksheet | 同じ workbook には複数のworksheet を保持することができ、 |  |
|  | 異なる種類のコンテンツを保持するために使用されます。 |  |
| Column | 列は垂直のデータの区分で、大文字で表されます。 | A, B, AA,AB |
| Row | 行は水平のデータの区分で数値で表されます。 | 1, 2 |
| Cell | ColumnとRowの組み合わせで指定した特定のセルを表します。  | A1, B2 |
| Value | セルに含まれているデータ |  |

重要なことは、OpenPyXLでデータを処理ためにはセルを移動させながらValueを参照/設定する必要があるということです。

### Excelファイルの読み込み
 `load_workbook()` にExcelファイルのパスを与えると　Workbookオブジェクトが返されます。アクティブになっているワークシートは  `.active` 属性を参照することで得られます。明示的にワークシートを指定することもできます。
ワークシートのサイズは Workbookオブジェクトの `.dimensions` 属性やワークシートの `.max_column` および `max_row` を参照すると知ることができます。


```
 In [2]: # %load c11_using_openpyxl.py
    ...: from openpyxl import load_workbook, Workbook
    ...:
    ...: wb = load_workbook('test.xlsx')
    ...: ws = wb.active
    ...:
    ...: print('\nUsing break')
    ...: for num, row in enumerate(ws.rows):
    ...:     if num >= 2:
    ...:         break
    ...:     print(row)
    ...:
    ...: print('\nUsing slice')
    ...: for row in ws['A1:G2']:
    ...:     print(row)
    ...:
    ...: print('\nCheck dimensions')
    ...: print(f'Dimensions: {ws.dimensions}')
    ...: print(f'Max Row: {ws.max_row}')
    ...: print(f'Max Column: {ws.max_column}')
    ...:
 
 Using break
 (<Cell 'Sheet1'.A1>, <Cell 'Sheet1'.B1>, <Cell 'Sheet1'.C1>, <Cell 'Sheet1'.D1>, <Cell 'Sheet1'.E1>, <Cell 'Sheet1'.F1>, <Cell 'Sheet1'.G1>)
 (<Cell 'Sheet1'.A2>, <Cell 'Sheet1'.B2>, <Cell 'Sheet1'.C2>, <Cell 'Sheet1'.D2>, <Cell 'Sheet1'.E2>, <Cell 'Sheet1'.F2>, <Cell 'Sheet1'.G2>)
 
 Using slice
 (<Cell 'Sheet1'.A1>, <Cell 'Sheet1'.B1>, <Cell 'Sheet1'.C1>, <Cell 'Sheet1'.D1>, <Cell 'Sheet1'.E1>, <Cell 'Sheet1'.F1>, <Cell 'Sheet1'.G1>)
 (<Cell 'Sheet1'.A2>, <Cell 'Sheet1'.B2>, <Cell 'Sheet1'.C2>, <Cell 'Sheet1'.D2>, <Cell 'Sheet1'.E2>, <Cell 'Sheet1'.F2>, <Cell 'Sheet1'.G2>)
 
 Check dimensions
 Dimensions: A1:G1809
 Max Row: 1809
 Max Column: 7
 
 In [3]:
 
```

 `read_workbook()` では次の引数を与えることができます。

  -  `read_only` -  `True` を与えるとリードオンリーモードでオープンする。デフォルトは  `False` 
  -  `data_only` -  `True` を与えると式は無視して値だけを読み込む。デフォルトは  `False` 

ワークシートで行や列を範囲指定することもできます。

セルの範囲や移動しただけでもメモリに展開されることに注意してください。
例えば次のようなコードはセルに対して何も処理していませんが、100x100セル分のメモリが使用されます。


```
 for x in range(1,101):
       for y in range(1,101):
            ws.cell(row=x, column=y)
```

行と列を取り出すメソッドが提供されていて、これらはジェネレーターとして機能します。

-  `.iter_rows()` 
-  `.iter_cols()` 

この2つのメソッドでは、範囲を指定できるように次のキーワード引数を受け取ります。

-  `min_row` 
-  `max_row` 
-  `min_col` 
-  `max_col` 


```
 In [2]: # %load c13_diff_intr_col_row.py
    ...: from openpyxl import load_workbook
    ...:
    ...: wb = load_workbook('test.xlsx')
    ...: ws = wb.active
    ...: ws.title = 'TSLA'
    ...:
    ...: print('\nusing iter_rows()')
    ...: for row in ws.iter_rows(min_row=1, max_row=2,
    ...:                         min_col=1, max_col=7):
    ...:     print(row)
    ...:
    ...: print('\nusing iter_cols()')
    ...: for column in ws.iter_cols(min_row=1, max_row=2,
    ...:                            min_col=1, max_col=7):
    ...:     print(column)
    ...:
 
 using iter_rows()
 (<Cell 'TSLA'.A1>, <Cell 'TSLA'.B1>, <Cell 'TSLA'.C1>, <Cell 'TSLA'.D1>, <Cell 'TSLA'.E1>, <Cell 'TSLA'.F1>, <Cell 'TSLA'.G1>)
 (<Cell 'TSLA'.A2>, <Cell 'TSLA'.B2>, <Cell 'TSLA'.C2>, <Cell 'TSLA'.D2>, <Cell 'TSLA'.E2>, <Cell 'TSLA'.F2>, <Cell 'TSLA'.G2>)
 
 using iter_cols()
 (<Cell 'TSLA'.A1>, <Cell 'TSLA'.A2>)
 (<Cell 'TSLA'.B1>, <Cell 'TSLA'.B2>)
 (<Cell 'TSLA'.C1>, <Cell 'TSLA'.C2>)
 (<Cell 'TSLA'.D1>, <Cell 'TSLA'.D2>)
 (<Cell 'TSLA'.E1>, <Cell 'TSLA'.E2>)
 (<Cell 'TSLA'.F1>, <Cell 'TSLA'.F2>)
 (<Cell 'TSLA'.G1>, <Cell 'TSLA'.G2>)
 
 In [3]:
 
```

-  `.iter_rows()` 選択した範囲の行ごとに1つのタプル要素を取得
-  `.iter_cols()` 指定した範囲の列ごとに1つのタプル要素を取得

これらのメソッドには、キーワード引数  `values_only` を渡すことができます。これを  `True` に設定すると、Cell オブジェクトではなく、セルの値を返すようになります。


```
 In [2]: # %load c14_openpyxl_valuesonly.py
    ...: from openpyxl import load_workbook
    ...:
    ...: wb = load_workbook('test.xlsx')
    ...: ws = wb.active
    ...:
    ...: for values in ws.iter_rows(min_row=1, max_col=7, max_row=2,
    ...:                         values_only=True):
    ...:     print(values)
    ...:
 ('Date', 'High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close')
 (datetime.datetime(2015, 1, 2, 0, 0), 44.65000152587891, 42.65200042724609, 44.57400131225586, 43.86199951171875, 23822000, 43.86199951171875)
 
 In [3]:
 
```

### 新規のワークブック/ワークシートを作成
新規のワークブックを作成するためには、 `Workbook` クラスのインスタンスオブジェクトを作成すると、
ワークシート  `Sheet` がデフォルトで作成されます。
 `create_sheet()` メソッドで明示的に名前を指定してワークシートを作成することができます。


```
 In [2]: # %load c15_openpyxl_create_wb.py
    ...: from openpyxl import Workbook
    ...:
    ...: wb = Workbook()
    ...:
    ...: names1 = wb.sheetnames
    ...:
    ...: ws = wb.active
    ...: v1 = ws.title
    ...:
    ...: ws = wb.create_sheet("TSLA")     # 最後に追加 (default)
    ...: v2 = ws.title
    ...:
    ...: names2 = wb.sheetnames
    ...: ws = wb.create_sheet("APPL",0)   # 指定位置に挿入
    ...: names3 = wb.sheetnames
    ...: ws = wb.create_sheet("MSFT",-1)  # 末尾からの指定位置に挿入
    ...: names4 = wb.sheetnames
    ...: del wb['Sheet']
    ...: names5 = wb.sheetnames
    ...:
    ...: # names1
    ...: # v1, v2
    ...: # names2
    ...: # names3
    ...: # names4
    ...: # names5
    ...:
    
 In [3]: names1
 Out[3]: ['Sheet']
 
 In [4]: v1, v2
 Out[4]: ('Sheet', 'TSLA')
 
 In [5]: names2
 Out[5]: ['Sheet', 'TSLA']
 
 In [6]: names3
 Out[6]: ['APPL', 'Sheet', 'TSLA']
 
 In [7]: names4
 Out[7]: ['APPL', 'Sheet', 'MSFT', 'TSLA']
 
 In [8]: names5
 Out[8]: ['APPL', 'MSFT', 'TSLA']
 
 In [9]:
```

### 行と列の管理
ワークシートの操作では、行や列を追加/削除がよくでてきます。これを行うためのメソッドが提供されています。

  -  `.insert_rows()` 　ー　指定した位置に空の行を挿入
  -  `.delete_rows()` 　ー　指定した位置の行を削除
  -  `.insert_cols()` 　ー　指定した位置に空のカラムを挿入
  -  `.delete_cols()` 　ー　指定した位置のカラムを削除

これらのメソッドは次の2つのキーワード引数を受け取ります。

  -  `idx` - インデックス　
  -  `amount` - データ量


```
 In [2]: # %load c16_openpyxl_insert_delete.ppy
    ...: from openpyxl import Workbook
    ...:
    ...: wb = Workbook()
    ...: ws = wb.active
    ...:
    ...: ws['A1'] = 'Python'
    ...: ws['B1'] = 'Osaka'
    ...: ws['A2'] = 'Hello'
    ...: ws['B2'] = 'World'
    ...:
    ...: def print_cell(sheet):
    ...:     for values in sheet.iter_rows(values_only=True):
    ...:         print(values)
    ...:
    ...: ws1 = wb.copy_worksheet(ws)
    ...: ws.insert_cols(idx=1, amount=2)
    ...: ws2 = wb.copy_worksheet(ws)
    ...: ws.insert_rows(idx=2)
    ...: ws3 = wb.copy_worksheet(ws)
    ...: ws.delete_cols(idx=1)
    ...: ws4 = wb.copy_worksheet(ws)
    ...: ws.delete_rows(idx=2)
    ...:
    ...: # print_cell(ws1)
    ...: # print_cell(ws2)
    ...: # print_cell(ws3)
    ...: # print_cell(ws4)
    ...: # print_cell(ws)
    ...: # print(wb.sheetnames)
    ...:
 
 In [3]: print_cell(ws1)
 ('Python', 'Osaka')
 ('Hello', 'World')
 
 In [4]: print_cell(ws2)
 (None, None, 'Python', 'Osaka')
 (None, None, 'Hello', 'World')
 
 In [5]: print_cell(ws3)
 (None, None, 'Python', 'Osaka')
 (None, None, None, None)
 (None, None, 'Hello', 'World')
 
 In [6]: print_cell(ws4)
 (None, 'Python', 'Osaka')
 (None, None, None)
 (None, 'Hello', 'World')
 
 In [7]: print_cell(ws)
 (None, 'Python', 'Osaka')
 (None, 'Hello', 'World')
 
 In [8]: print(wb.sheetnames)
 ['Sheet', 'Sheet Copy', 'Sheet Copy1', 'Sheet Copy2', 'Sheet Copy3']
 
 In [9]:
 
```

### データの追加と抽出
ワークシートにデータを追加するときは、 `.append()` メソッドを使用します。


```
 In [2]: # %load c17_openpyxl_create_append.py
    ...: from openpyxl import Workbook
    ...:
    ...: wb = Workbook()
    ...: ws = wb.active
    ...:
    ...: ws.append(['This is A1', 'This is B1', 'This is C1'])
    ...: ws.append({'A' : 'This is A1', 'C' : 'This is C1'})
    ...: ws.append({1 : 'This is A1', 3 : 'This is C1'})
    ...:
    ...: values = ws.iter_rows(min_row=1, values_only=True)
    ...: for val in values:
    ...:     print(val)
    ...:
 ('This is A1', 'This is B1', 'This is C1')
 ('This is A1', None, 'This is C1')
 ('This is A1', None, 'This is C1')
 
 In [3]:
 
```

さて、カラム  `Adj Close` の値が100ドル以下のデータを抜き出してみましょう。こうした場合通常であれば、pandas のDataFrame を使う方が読みやすくコードも簡潔に書くことができますが、使わない場合のコードは次のようになります。


```
 In [2]: # %load c18_openpyxl_extraction.py
    ...: from openpyxl import load_workbook
    ...:
    ...: wb = load_workbook('test.xlsx')
    ...: ws = wb.active
    ...:
    ...: data = list()
    ...: column_names = ws.iter_rows(min_row=1, max_row=1,
    ...:                             max_col=7, values_only=True).__next__()
    ...: data.append(column_names)
    ...:
    ...: values = ws.iter_rows(min_row=2, max_col=7, values_only=True)
    ...: for val in values:
    ...:     if val[6] < 100:
    ...:         data.append(val)
    ...:
    ...: # len(data)
    ...: # data[0]
    ...: # data[-1]
    ...:
 
 In [3]: len(data)
 Out[3]: 1275
 
 In [4]: data[0]
 Out[4]: ('Date', 'High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close')
 
 In [5]: data[-1]
 Out[5]:
 (datetime.datetime(2020, 4, 3, 0, 0),
  103.0979995727539,
  93.6780014038086,
  101.9000015258789,
  96.00199890136719,
  112810500,
  96.00199890136719)
 
 In [6]:
 
```

 `iter_rows()` メソッドはジェネレーターであるため、for文で処理されるか  `__next()__` が呼ばれないと値を返さないことに注意してください。

 ipython
```
 In [2]: # %load c19_openpyxl_extract_save.py
    ...: from openpyxl import load_workbook, Workbook
    ...: from dataclasses import dataclass
    ...: from datetime import datetime
    ...:
    ...: wb = load_workbook('test.xlsx')
    ...: ws = wb.active
    ...:
    ...: stock_data = list()
    ...: columns_names = ws.iter_rows(min_row=1, max_row=1,
    ...:                              max_col=7, values_only=True).__next__()
    ...:
    ...: values = ws.iter_rows(min_row=2, max_col=7, values_only=True)
    ...: for val in values:
    ...:     if val[6] < 100:
    ...:         stock_data.append(val)
    ...:
    ...: new_wb = Workbook()
    ...: new_ws = new_wb.active
    ...:
    ...: for data in stock_data:
    ...:     new_ws.append(data)
    ...:
    ...: new_wb.save('output2.xlsx')
    ...:
    ...: wb2 = load_workbook('output2.xlsx')
    ...: ws2 = wb2.active
    ...:
    ...: # ws2.dimensions
    ...: # ws2.max_row
    ...: # ws2.max_column
    ...: # data
    ...:
 
 In [3]: ws2.dimensions
 Out[3]: 'A1:G1274'
 
 In [4]: ws2.max_row
 Out[4]: 1274
 
 In [5]: ws2.max_column
 Out[5]: 7
 
 In [6]: data
 Out[6]:
 (datetime.datetime(2020, 4, 3, 0, 0),
  103.0979995727539,
  93.6780014038086,
  101.9000015258789,
  96.00199890136719,
  112810500,
  96.00199890136719)
 
 In [7]:
```

単純にリストやタプルでデータを保持するよりも、dataclass を用たクラスを定義するともっとデータを把握しやすくなります。


```
 In [2]: # %load c20_openpyxl_dataclass.py
    ...: from openpyxl import load_workbook, Workbook
    ...: from dataclasses import dataclass
    ...: from datetime import datetime
    ...:
    ...: @dataclass
    ...: class StockPrice:
    ...:     date: datetime
    ...:     hight: int
    ...:     low: int
    ...:     open: int
    ...:     close: int
    ...:     volume: int
    ...:     adjClose: int
    ...:
    ...:     def value(self):
    ...:         return (self.date, self.hight, self.open, self.close,
    ...:                 self.volume, self.adjClose )
    ...:
    ...:
    ...: wb = load_workbook('test.xlsx')
    ...: ws = wb.active
    ...:
    ...: data = list()
    ...: columns_names = ws.iter_rows(min_row=1, max_row=1,
    ...:                              max_col=7, values_only=True).__next__()
    ...:
    ...: values = ws.iter_rows(min_row=2, max_col=7, values_only=True)
    ...: for val in values:
    ...:     if val[6] < 100:
    ...:         data.append(StockPrice(*val))
    ...:
    ...: # data[-1]
    ...: # data[-1].value()
    ...: # data[-1].adjClose
    ...:
 
 In [3]: data[-1]
 Out[3]: StockPrice(date=datetime.datetime(2020, 4, 3, 0, 0), hight=103.0979995727539, low=93.6780014038086, open=101.9000015258789, close=96.00199890136719, volume=112810500, adjClose=96.00199890136719)
 
 In [4]: data[-1].value()
 Out[4]:
 (datetime.datetime(2020, 4, 3, 0, 0),
  103.0979995727539,
  101.9000015258789,
  96.00199890136719,
  112810500,
  96.00199890136719)
 
 In [5]: data[-1].adjClose
 Out[5]: 96.00199890136719
 
 In [6]:
```

### OpenPyXLでチャートを追加
Python には便利で利用が簡単な可視化ライブラリがあります。同じ理由で、データを可視化チャート表示があるでしょう。大量のデータを視覚化して把握しやすくすることができます。
棒グラフ(Bar Char)、円グラフ(Pie Char)、折れ線グラフ(Line Char)など、さまざまな種類のチャートがあります。openpyxlでは次の種類のチャートをワークシート追加させることができます。

サポートしているチャート
  - area_chart　ー　面グラフ
  - bar_chart　ー　棒グラフ
  - bubble_chart　ー　バブルチャート
  - line_chart　ー　折れ線グラフ
  - pie_chart　ー　円グラフ
  - radar_chart ー　レーダーチャート
  - scatter_chart　ー　散布図
  - stock_chart　ー	株価グラフ
  - surface_chart　ー　等高線グラフ

Excelで利用できる全ての種類のチャートをサポートしているわけではなくて、Funnel、Gantt、Pareto、Treemap、Waterfall、Map、Sunburstはサポートされていないことに注意してください。

チャートを作成するためには、チャートの種類を定義する必要があります。BarChart、LineChartなどのチャートの種類と、チャートに使用するデータ（Referenceと呼びます）を定義します。チャートに表示するデータが定義されている必要があります。データをそのまま使えることもありますが、追加情報を得るためにデータを少し加工する必要がある場合もあります。

サンプルのExcelファイル `test.xlsx` の  `Adj Clsoe` の値を可視化してみましょう。


```
 In [2]: # %load c21_openpyxl_linechart.py
    ...: from openpyxl import load_workbook, Workbook
    ...: from openpyxl.chart import LineChart, Reference
    ...:
    ...: wb = load_workbook('test.xlsx')
    ...: ws = wb.active
    ...:
    ...: chart = LineChart()
    ...: chart.width = 20    # default is 15
    ...: chart.height = 15   # default is 7
    ...: chart.title = 'TSLA StockChart'
    ...: chart.x_axis.title = 'Date'
    ...: chart.y_axis.title = 'Adj Close Price'
    ...: chart.legend.position = 'b'
    ...:
    ...: data = Reference(worksheet=ws,
    ...:                 min_row=1, max_row=ws.max_row,
    ...:                 min_col=ws.max_column, max_col=ws.max_column)
    ...: category = Reference(worksheet=ws,
    ...:                 min_row=2, max_row=ws.max_row,
    ...:                 min_col=1, max_col=1)
    ...:
    ...: chart.add_data(data, titles_from_data=True)
    ...: chart.set_categories(category)
    ...:
    ...: ws.add_chart(chart, 'I2')
    ...: wb.save('TSLA.xlsx')
    ...:
 
 In [3]:
```

このコードを実行して作成される  `TSLA.xlslx` をExcel で開くと次のようになっています。


![](https://gyazo.com/72d6f5bd8ff29d628107e273bc5a85d5.png)


 `chart.legend.position` は凡例の配置場所を次の値で指定します。

  -  `'t'` ー　チャート上部に配置 (top)
  -  `'b'` ー　チャート下部に配置 (bottom)
  -  `'l'` ー　チャート左側に配置 (left)
  -  `'r'` ー　チャート右側に配置 (right)
  -  `None` ー　凡例を非表示

### 数式の扱い

OpenPyXL でセルに数式を書き込むときは、単純に文字列として値をセットするだけです。読み込んだときも、ワークシートのセルに数式があるときは文字列として読み出します。


```
 In [2]: # %load c23_openyxl_addd_formula.py
    ...: from openpyxl import load_workbook, Workbook
    ...:
    ...: wb = Workbook()
    ...: ws = wb.active
    ...:
    ...: data = (10, 20, 30, 40)
    ...:
    ...: ws.append(data)
    ...: ws['A2'] = '=SUM(A1:D1)'
    ...:
    ...: wb.save('output_formula.xlsx')
    ...:
    ...: wb2 = load_workbook('output_formula.xlsx')
    ...: ws2 = wb2.active
    ...:
    ...: wb3 = load_workbook('output_formula.xlsx', data_only=True)
    ...: ws3 = wb3.active
    ...:
    ...: # ws2['A2'].value
    ...: # ws3['A2'].value
    ...:
 
 In [3]: ws2['A2'].value
 Out[3]: '=SUM(A1:D1)'
 
 In [4]: ws3['A2'].value
 
 In [5]: print(ws3['A2'].value)
 None
 
 In [6]:
 
```


![](https://gyazo.com/de70194245e84b8cc2023edb0a9a8fc1.png)

 `load_workbook()` に  `data_only=True` を与えた場合、そのExcelファイルがExcelによって開かれて、かつ保存されていれば計算結果を得ることができますが、今回のようにExcelで処理される前であれば `None` が返されます。書くまでも数式を計算するのはExcelというわけです。

OpenPyXLではExeclの数式は限定的な解釈しかしてくれません。[ドキュメント　](https://openpyxl.readthedocs.io/en/latest/formula.html) にある例をみてましょう。


```
 In [2]: # %load c22_openpyxl_formulae.py
    ...: from openpyxl import Workbook
    ...: from openpyxl.utils import FORMULAE
    ...: from openpyxl.formula import Tokenizer
    ...:
    ...: formula = """=IF($A$1,"then True",MAX(DEFAULT_VAL,'Sheet 2'!B1))"""
    ...: tok = Tokenizer(formula)
    ...:
    ...: print("\n".join("%12s%11s%9s" % (t.value, t.type, t.subtype) for t in to
    ...: k.items))
    ...:
    ...: # FORMULAE
    ...:
    ...:
    ...:
          IF(       FUNC     OPEN
         $A$1    OPERAND    RANGE
            ,        SEP      ARG
  "then True"    OPERAND     TEXT
            ,        SEP      ARG
         MAX(       FUNC     OPEN
  DEFAULT_VAL    OPERAND    RANGE
            ,        SEP      ARG
 'Sheet 2'!B1    OPERAND    RANGE
            )       FUNC    CLOSE
            )       FUNC    CLOSE
 
 In [3]: FORMULAE
 Out[3]:
 frozenset({'ABS',
            'ACCRINT',
            'ACCRINTM',
            'ACOS',
            'ACOSH',
            'AMORDEGRC',
            'AMORLINC',
            'AND',
  (以下略)
                
```

この例では、数式　 `=IF($A$1,"then True",MAX(DEFAULT_VAL,'Sheet 2'!B1))` を構文解釈した結果を返すものです。 `IF` などの関数は  `from openpyxl.utils import FORMULAE` に定義されているものであれば「構文解釈」まではしてくれます。そうです、OpenPyXLではここまでしかサポートしていません。この式を解釈して計算処理してくれるわけではないことに注意しましょう。Excelの数式を解釈して計算するコードを書くことはおすすめしません。
こうした場合は次で説明する pycel や xlcalculator を使うことを検討してみてください。また、マクロは xlwings を使うと処理することができますが、使用しているプラットフォームでExcelがインストールされている必要があります。

## Pycel を使ってExcelの数式を処理する

Pycel はExcelの数式をExcelに依存せずに、つまりPythonで処理するためのライブラリです。
主なな数学関数 ( `sin` ,  `cos` ,  `atan2` , ...) と演算子 ( `+` ,  `/` ,  `^` , ...) はすべてサポートされており、範囲 ( `A5:D7` ) や  `MIN` ,  `MAX` ,  `INDEX,`  `LOOKUP` ,  `LINEST` といった関数もサポートされています。
コードベースは小さく、比較的高速で、理解しやすく、拡張しやすくなっているので、サポートされていない関数があったとしても少ない労力で実装するこができます。

### インストール
pycel のインストールは pip コマンドで行います。

 bash
```
 $ pip install pycel
 
```

### pycel の使用方法

前述の `output_formula.xlsx` で確認してみます。


```
 In [2]: # %load c30_pycel_demo.py
    ...: from pycel import ExcelCompiler
    ...:
    ...: # See Also: c22_openpyxl_addd_formula.py
    ...:
    ...: excel = ExcelCompiler('output_formula.xlsx')
    ...:
    ...: val1 = excel.evaluate('Sheet!A1')
    ...: val2 = excel.evaluate('Sheet!A2')
    ...:
    ...: excel.set_value('Sheet!A1', 100)
    ...: val3 = excel.evaluate('Sheet!A1')
    ...: val4 = excel.evaluate('Sheet!A2')
    ...:
    ...: # val1
    ...: # val2
    ...: # val3
    ...: # val4
    ...:
 
 In [3]: val1
 Out[3]: 10
 
 In [4]: val2
 Out[4]: 100
 
 In [5]: val3
 Out[5]: 100
 
 In [6]: val4
 Out[6]: 190
 
 In [7]:
 
```


このワークシートの  `A2` には  `=SUM(A1:D1)` の数式が入っているのですが、計算結果が得られています。また、A1`のセルの値を変更した場合も、それ内容が反映された結果が得られます。

## xlcalculator で数式を処理する

[xlcalculator ](https://pypi.org/project/xlcalculator/)  は、Excelファイルを読み込み、サポートされている関数の範囲内で、Excel関数をPythonコードに変換し、その後、生成されたPythonコードを評価することができるPythonライブラリです。基本的には、Excelを使わずにExcelの計算を行うことができます。


### インストール
xlcalculator のインストールは pip コマンドで行います。

 bash
```
 $ pip install xlcalculator
 
```

### xlcalculator の使用方法

前述の `output_formula.xlsx` で確認してみます。


```
 In [2]: # %load c31_xlcalculator.py
    ...: from xlcalculator import ModelCompiler, Evaluator, Model
    ...:
    ...: workbook_path = './output_formula.xlsx'
    ...: compiler = ModelCompiler()
    ...: new_model = compiler.read_and_parse_archive(workbook_path)
    ...: evaluator = Evaluator(new_model)
    ...: val1 = evaluator.evaluate('Sheet!A1').value
    ...: val2 = evaluator.evaluate('Sheet!A2').value
    ...:
    ...: evaluator.set_cell_value('Sheet!A1', 100)
    ...: val3 = evaluator.evaluate('Sheet!A1').value
    ...: val4 = evaluator.evaluate('Sheet!A2').value
    ...:
    ...: # val1
    ...: # val2
    ...: # val3
    ...: # val4
    ...:
 
 In [3]: val1
 Out[3]: 10
 
 In [4]: val2
 Out[4]: 100
 
 In [5]: val3
 Out[5]: 100
 
 In [6]: val4
 Out[6]: 190
 
 In [7]:
 
```

このワークシートの  `A2` には  `=SUM(A1:D1)` の数式が入っているのですが、計算結果が得られています。また、A1`のセルの値を変更した場合も、それ内容が反映された結果が得られます。


次のようにクラス定義をするとコードが読みやすくなります。


```
 In [2]: # %load c32_xlcalculator_class.py
    ...: from xlcalculator import ModelCompiler, Evaluator, Model
    ...: from typing import Optional
    ...:
    ...: class Workbook:
    ...:     def __init__(self,
    ...:                  workbook: str = "./sample.xlsx",
    ...:                  evaluator: Optional[Evaluator] = None):
    ...:         if evaluator:
    ...:             self.evaluator = evaluator
    ...:         else:
    ...:             compiler = ModelCompiler()
    ...:             new_model = compiler.read_and_parse_archive(workbook)
    ...:             self.evaluator = Evaluator(new_model)
    ...:         self.workbook = workbook
    ...:         self.worksheet = None
    ...:
    ...:     def get_cell_value(self,
    ...:                        worksheet: Optional[str]=None,
    ...:                        address: str='A1'):
    ...:         if worksheet:
    ...:             self.worksheet = worksheet
    ...:
    ...:         return (self.evaluator
    ...:                 .evaluate(f"{self.worksheet}!{address}")
    ...:                 .value)
    ...:
    ...:     def set_cell_value(self,
    ...:                        worksheet: Optional[str]=None,
    ...:                        address: str='A1',
    ...:                        value: str=0):
    ...:         if worksheet:
    ...:             self.worksheet = worksheet
    ...:
    ...:         self.evaluator.set_cell_value(
    ...:                            f"{self.worksheet}!{address}",
    ...:                            value)
    ...:
    ...: wb = Workbook('output_formula.xlsx')
    ...:
    ...: val1 = wb.get_cell_value(worksheet='Sheet', address='A1')
    ...: val2 = wb.get_cell_value(address='A2')
    ...: wb.set_cell_value(address='A1', value=100)
    ...: val3 = wb.get_cell_value(address='A2')
    ...:
    ...: # val1
    ...: # val2
    ...: # val3
    ...:
 
 In [3]: val1
 Out[3]: 10
 
 In [4]: val2
 Out[4]: 100
 
 In [5]: val3
 Out[5]: 190
 
 In [6]:
 
```

## Excel関数のサポート比較
xlcalcurator と PyCel がサポートしているExcel関数について次表にまとめます。

 互換性関連

| 関数 |  xlcalculator | PyCel |
|:--|:--|:--|
| FLOOR | Y | Y |

 日時関連

| 関数 |  xlcalculator | PyCel |
|:--|:--|:--|
| DATE  | Y    | Y |
| DATEDIF  | Y    | N |
| DATEVALUE    | N    | Y |
| DAY      | Y    | Y |
| DAYS     | Y    | N |
| EDATE    | Y    | Y |
| EOMONTH  | Y    | Y |
| HOUR     | N    | Y |
| ISOWEEKNUM   | Y    | N |
| MINUTE       | N    | Y |
| MONTH    | Y    | Y |
| NOW  | Y    | Y |
| SECOND    | N   | Y |
| TIME         | N    | N |
| TIMEVALUE    | N    | Y |
| TODAY    | Y    | Y |
| WEEKDAY      | Y    | Y |
| YEAR         | Y    | Y |
| YEARFRAC     | Y    | Y |

 工学関連

| 関数 |  xlcalculator | PyCel |
|:--|:--|:--|
| BIN2DEC  | Y   |  Y |
| BIN2HEX  | Y    | Y |
| BIN2OCT  | Y    | Y |
| DEC2BIN  | Y    | Y |
| DEC2HEX  | Y    | Y |
| DEC2OCT  | Y    | Y |
| HEX2BIN  | Y    | Y |
| HEX2DEC  | Y    | Y |
| HEX2OCT  | Y    | Y |
| OCT2BIN  | Y    | Y |
| OCT2DEC  | Y    | Y |
| OCT2HEX  | Y    | Y |

 金関関連

| 関数 |  xlcalculator | PyCel |
|:--|:--|:--|
| RR   | Y    | N |
| NPV  | Y    | Y |
| PMT  | Y   |  N |
| PV   | Y    | N |
| SLN  | Y    | N |
| VDB  | Y    | N |
| XIRR     | N    | N |
| XNPV     | Y    | N |

 数学関連

| 関数 |  xlcalculator | PyCel |
|:--|:--|:--|
| ABS  | Y    | Y |
| ACOS     | Y    | N |
| ACOSH    | Y    | N |
| ACOT     | N    | N |
| ACOTH    | N    | N |
| ARABIC   | N    | N |
| ASIN     | N    | N |
| ASINH    | Y    | N |
| ATAN     | Y    | N |
| ATAN2    | Y    | Y |
| ATANH    | N    | N |
| CEILING  | Y    | Y |
| CEILING.MATH     | N    | Y |
| CEILING.PRECISE      | N    | Y |
| COS  | Y    | N |
| COSH     | Y    | N |
| COT      | N    | N |
| COTH     | N    | N |
| CSC      | N    | N |
| CSCH     | N    | N |
| DECIMAL      | N    | N |
| DEGREES  | Y    | N |
| EVEN     | Y    | Y |
| EXP  | Y    | N |
| FACT     | Y    | Y |
| FACTDOUBLE   | Y    | Y |
| FLOOR.MATH   | N    | Y |
| FLOOR.PRECISE    | N    | Y |
| GCD  | N    | N |
| INT      | Y    | Y |
| ISO.CEILING  | N    | N |
| LCM  | N    | N |
| LN   | Y    | Y |
| LOG  | Y    | Y |
| LOG10    | Y    | N |
| MOD  | Y    | Y |
| MROUND   | N    | N |
| ODD  | N    | Y |
| PI   | Y    | N |
| POWER    | Y    | Y |
| RADIANS  | Y    | N |
| RAND     | Y    | N |
| RANDBETWEEN  | Y    | N |
| ROMAN    | N    | N |
| ROUND    | Y    | Y |
| ROUNDDOWN    | Y    | Y |
| ROUNDUP  | Y    | Y |
| SEC      | N    | N |
| SECH     | N    | N |
| SIGN     | Y    | Y |
| SIN  | Y    | N |
| SINH     | N    | N |
| SQRT     | Y    | N |
| SQRTPI   | Y    | N |
| SUM  | Y    | Y |
| SUMIF    | Y   |  Y |
| SUMIFS   | Y    | Y |
| SUMPRODUCT   | Y    | Y |
| TAN  | Y    | N |
| TANH    |  N    | N |
| TRUNC    | Y    | Y |

 統計関連

| 関数 |  xlcalculator | PyCel |
|:--|:--|:--|
| AVERAGE  | Y    | Y |
| AVERAGEA     | N    | N |
| AVERAGEIF    | N    | Y |
| AVERAGEIFS   | N    | Y |
| COUNT    | Y    | Y |
| COUNTA   | Y    | N |
| COUNTBLANK   | N    | N |
| COUNTIF  | Y    | Y |
| COUNTIFS     | Y    | Y |
| LARGE    | N    | Y |
| LINEST       | N    | Y |
| MAX      | Y    | Y |
| MAXA     | N    | N |
| MAXIFS   | N    | Y |
| MIN  | Y    | Y |
| MINA     | N    | N |
| MINIFS    | N   | Y |
| SMALL    | N    | Y |

 文字列操作関連

| 関数 |  xlcalculator | PyCel |
|:--|:--|:--|
| CONCAT   | Y    | Y |
| CONCATENATE  | Y |  Y |
| EXACT    | Y    | N |
| FIND     | Y    | Y |
| LEFT     | Y    | Y |
| LEN  | Y    | Y |
| LOWER    | Y    | Y |
| MID  | Y    | Y |
| REPLACE  | Y   | Y |
| RIGHT    | Y   | Y |
| TRIM     | Y    | Y |
| UPPER    | Y    | Y |
| VALUE        | N    | Y |

 論理演算関連

| 関数 |  xlcalculator | PyCel |
|:--|:--|:--|
| AND  | Y    | Y |
| FALSE    | Y    | N |
| IF   | Y    | Y |
| IFERROR      | N    | Y |
| IFS      | N    | Y |
| NOT      | N    | Y |
| OR   | Y    | Y |
| SWITCH       | N    | N |
| TRUE     | Y    | N |
| XOR      | N    | Y |

 セル情報関連

| 関数 |  xlcalculator | PyCel |
|:--|:--|:--|
| ISBLANK  | Y    | N |
| ISERR    | Y    | Y |
| ISERROR  | Y    | Y |
| ISEVEN   | Y    | Y |
| ISNA     | Y    | Y |
| ISNUMBER     | Y    | Y |
| ISODD    | Y    | Y |
| ISTEXT   | Y    | Y |
| NA   | Y    | N |

 セル選択関連

| 関数 |  xlcalculator | PyCel |
|:--|:--|:--|
| CHOOSE  |  Y    | N |
| COLUMN   | N    | Y |
| COLUMNS  | N    | N |
| HLOOKUP  | N    | Y |
| INDEX    | N    | Y |
| INDIRECT     | N    | Y |
| LOOKUP       | N    | Y |
| MATCH    | Y    | Y |
| OFFSET       | N    | Y |
| ROW      | N    | Y |
| ROWS     | N    | Y |
| VLOOKUP  | Y    | Y |

 両方ともサポートしていない関数一覧

| 関数 |  xlcalculator | PyCel |
|:--|:--|:--|
| TIME | N   | N |
| XIRR   | N   | N |
| SWITCH | N   | N |
| COLUMNS  | N   | N |
| ACOT   | N   | N |
| ACOTH   | N   | N |
| ARABIC  | N   | N |
| ASIN   | N   | N |
| ATANH   | N   | N |
| COT   | N   | N |
| COTH   | N   | N |
| CSC   | N   | N |
| CSCH   | N   | N |
| DECIMAL   | N   | N |
| GCD  | N  |  N |
| ISO.CEILING  | N   | N |
| LCM  | N   | N |
| MROUND  | N   | N |
| ROMAN   | N   | N |
| SEC   | N   | N |
| SECH   | N  |  N |
| SINH   | N   | N |
| TANH   | N   | N |
| AVERAGEA   | N   | N |
| COUNTBLANK  | N   | N |
| MAXA   | N   | N |
| MINA   | N   | N |


## xlwings を使ってマクロを処理する
[xlwings ](https://www.xlwings.org/) を使うと、Python から Excel を実行して結果を取得することができます。有償のPRO版ではGoogle Spredsheet もサポートしています。しかし、Excel をバックエンドで実行するため、Excelがインストールされていないプラットフォームや、Linux などのように対応するExcelがリリースされていないプラットフォームでは利用することができません。


```
 In [2]: # %load c33_xlwings_demo.py
    ...: import xlwings as xw
    ...:
    ...: wb = xw.Book('output_formula.xlsx')
    ...: ws = wb.sheets.active
    ...: # ws = wb.sheets['Sheet']
    ...: # ws = wb.sheets[0]
    ...:
    ...: val1 = ws.range('A1').value
    ...: val2 = ws.range('A2').value
    ...:
    ...: val3 = ws.range('A1').value = 100
    ...: val4 = ws.range('A2').value
    ...:
    ...: # val1
    ...: # val2
    ...: # val3
    ...: # val4
    ...: # wb.close()
    ...:
 
 In [3]: val1
 Out[3]: 10.0
 
 In [4]: val2
 Out[4]: 100.0
 
 In [5]: val3
 Out[5]: 100
 
 In [6]: val4
 Out[6]: 190.0
 
 In [7]: wb.close()
 
```

このコードを実行すると Excel が起動されます。 `.close()` メソッドを呼び出すと Excel は終了します。

### xlwings のコンバーター機能
xlwings は強力なコンバーター機能があるため、Numpy arraysやPandas DataFramesなどデータ型を、ExcelとPythonで双方向に変換することができます。


```
 In [2]: # %load c34_xlwings_pandas.py
    ...: import xlwings as xw
    ...: import pandas as pd
    ...:
    ...: wb = xw.Book('test.xlsx')
    ...: ws = wb.sheets.active
    ...:
    ...: df = ws.range('A1:G10').options(pd.DataFrame, header=1).value
    ...:
    ...: # df
    ...: # wb.close()
    ...:
 
 In [3]: df
 Out[3]:
                  High        Low       Open      Close      Volume  Adj Close
 Date
 2015-01-02  44.650002  42.652000  44.574001  43.862000  23822000.0  43.862000
 2015-01-05  43.299999  41.431999  42.910000  42.018002  26842500.0  42.018002
 2015-01-06  42.840000  40.841999  42.012001  42.256001  31309500.0  42.256001
 2015-01-07  42.956001  41.956001  42.669998  42.189999  14842000.0  42.189999
 2015-01-08  42.759998  42.001999  42.562000  42.124001  17212500.0  42.124001
 2015-01-09  41.995998  40.992001  41.784000  41.332001  23341500.0  41.332001
 2015-01-12  40.894001  39.849998  40.610001  40.442001  29751500.0  40.442001
 2015-01-13  41.521999  40.181999  40.664001  40.849998  22386500.0  40.849998
 2015-01-14  39.040001  37.000000  37.166000  38.537998  57759500.0  38.537998
 
 In [4]: wb.close()
 
 In [5]:
```

### Excel から Python を実行
コマンド ラインクツール xlwings が提供されています。

 bash
```
 $ xlwings --help
 xlwings version: 0.27.1
 usage: xlwings [-h]
                {addin,quickstart,runpython,restapi,license,config,code,permission,release,copy,vba}
                ...
 
 positional arguments:
   {addin,quickstart,runpython,restapi,license,config,code,permission,release,copy,vba}
     addin               Run "xlwings addin install" to install the Excel add-
                         in (will be copied to the XLSTART folder). Instead of
                         "install" you can also use "update", "remove" or
                         "status". Note that this command may take a while. You
                         can install your custom add-in by providing the name
                         or path via the --file/-f flag, e.g. "xlwings add-in
                         install -f custom.xlam or copy all Excel files in a
                         directory to the XLSTART folder by providing the path
                         via the --dir flag."
     quickstart          Run "xlwings quickstart myproject" to create a folder
                         called "myproject" in the current directory with an
                         Excel file and a Python file, ready to be used. Use
                         the "--standalone" flag to embed all VBA code in the
                         Excel file and make it work without the xlwings add-
                         in. Use "--fastapi" for creating a project that uses a
                         remote Python interpreter. Use "--addin --ribbon" to
                         create a template for a custom ribbon addin. Leave
                         away the "--ribbon" if you don't want a ribbon tab.
     runpython           macOS only: run "xlwings runpython install" if you
                         want to enable the RunPython calls without installing
                         the add-in. This will create the following file:
                         ~/Library/Application
                         Scripts/com.microsoft.Excel/xlwings-x.x.x.applescript
     restapi             Use "xlwings restapi run" to run the xlwings REST API
                         via Flask development server. Accepts "--host" and "--
                         port" as optional arguments.
     license             xlwings PRO: Use "xlwings license update -k KEY" where
                         "KEY" is your personal (trial) license key. This will
                         update ~/.xlwings/xlwings.conf with the LICENSE_KEY
                         entry. If you have a paid license, you can run
                         "xlwings license deploy" to create a deploy key. This
                         is not available for trial keys.
     config              Run "xlwings config create" to create the user config
                         file (~/.xlwings/xlwings.conf) which is where the
                         settings from the Ribbon add-in are stored. It will
                         configure the Python interpreter that you are running
                         this command with. To reset your configuration, run
                         this with the "--force" flag which will overwrite your
                         current configuration.
     code                Run "xlwings code embed" to embed all Python modules
                         of the workbook's dir in your active Excel file. Use
                         the "--file/-f" flag to only import a single file by
                         providing its path. Requires xlwings PRO.
     permission          "xlwings permission cwd" prints a JSON string that can
                         be used to permission the execution of all modules in
                         the current working directory via GET request.
                         "xlwings permission book" does the same for code that
                         is embedded in the active workbook.
     release             Run "xlwings release" to configure your active
                         workbook to work with a one-click installer for easy
                         deployment. Requires xlwings PRO.
     copy                Run "xlwings copy os" to copy the xlwings Office
                         Scripts module. Run "xlwings copy gs" to copy the
                         xlwings Google Apps Script module.
     vba                 This functionality allows you to easily write VBA code
                         in an external editor: run "xlwings vba edit" to
                         update the VBA modules of the active workbook from
                         their local exports everytime you hit save. If you run
                         this the first time, the modules will be exported from
                         Excel into your current working directory. To
                         overwrite the local version of the modules with those
                         from Excel, run "xlwings vba export". To overwrite the
                         VBA modules in Excel with their local versions, run
                         "xlwings vba import". The "--file/-f" flag allows you
                         to specify a file path instead of using the active
                         Workbook. Requires "Trust access to the VBA project
                         object model" enabled. NOTE: Whenever you change
                         something in the VBA editor (such as the layout of a
                         form or the properties of a module), you have to run
                         "xlwings vba export".
 
 options:
   -h, --help            show this help message and exit
   
```

 `xlwings quickstart PROJECTNAME` 実行すれば、簡単に新しいプロジェクトを作成できます。

 bash
```
 $ xlwings quickstart myproject
 xlwings version: 0.27.1
 $ ls myproject
 myproject.py   myproject.xlsm
 $ cat myproject/myproject.py
 import xlwings as xw
 
 
 def main():
     wb = xw.Book.caller()
     sheet = wb.sheets[0]
     if sheet["A1"].value == "Hello xlwings!":
         sheet["A1"].value = "Bye xlwings!"
     else:
         sheet["A1"].value = "Hello xlwings!"
 
 
 if __name__ == "__main__":
     xw.Book("myproject.xlsm").set_mock_caller()
     main()
     
```


xlwingsのアドインをインストールすることで、 Run main ボタン、 RunPython および UDF が使えるようになり、Excel から Python を実行させることができるようになります。

アドインのインストールは  `xlwings addin install` を実行します。

 bash
```
 $ xlwings addin install
 xlwings version: 0.27.1
 Successfully installed the xlwings add-in! Please restart Excel.
 Successfully enabled RunPython!
 
```

このコマンドは、Pythonのインストール ディレクトリからExcelの XLSTART ディレクトリに、アドインをコピーします。 次に、ワークブックで RunPython や UDFs を使用するために、VBAエディタの参照設定に xlwings を追加します。次のスクリーンショットを参照してください。(Windows: メニュー「ツール > 参照設定」、Mac: VBAエディタの左下の角)
前述した `xlwings quickstart` で作成したワークブックであれば、参照設定への追加は必要ありません。

![](https://gyazo.com/e6b58e77e3468a2852790e6d826af37c.png)

アドインは、パスワード xlwings でパスワード保護されています。デバッグまたは機能追加を行うには、保護を解除してください。もしくは、  `xlwings addin install --unprotected` でアドインをインストールすることもできます。

Pythonのコードを実行する一番簡単な方法は、Run main ボタンです。このボタンは、ワークブックと同じ名前のPythonモジュールにある main 関数を実行します。この方法なら、マクロが無効化された xlsx 形式でワークブックを保存できます。また、 xlwings quickstart コマンドから、 Run ボタンが自動的に機能するワークブックを作成することもできます。

![](https://gyazo.com/f6d87307048181c2e97e365b446717d5.png)
VBAエディタ ( `Alt-F11` )で、以下のコードをVBAモジュールに書き込んでみましょう。

 VBA
```
 Sub HelloWorld()
     RunPython "import hello; hello.world()"
 End Sub
 
```

このVBAスクリプトは  `hello.py` の関数  `world()` を呼び出します。

 hello.py
```
 # hello.py
 import numpy as np
 import xlwings as xw
 
 def world():
     wb = xw.Book.caller()
     wb.sheets[0].range('A1').value = 'Hello World!'
     
```

 `xlwings quickstart` コマンドで作成したプロジェクトでは、サンプル コール付きの新しいモジュールが自動的に追加されています。ゼロから作成したい場合は、 Excelのメニューで、「挿入 > 標準モジュール」 から新しいモジュールを追加します。

VBAの `HelloWorld` をボタンに設定することや、VBAエディタ上で  `F5` を押下して実行することもできます。

RunPython が呼び出す関数に引数を含めることは可能ですが、使い勝手が悪くなることに留意してください。また、 RunPython には戻り値がありません。Windows ではユーザー定義関数 (UDF)を使うことで解決できます。MacではUDFが利用できません。


## pyxlsb で Excel Binary Workbook を扱う

 `test.xlsb` は  `test.xlsx` を Excel で開いて、Excel Binary Workbook として保存したものです。
ファイルの内容を確認すると `.xlsx` と異なっていることが確認できます。

 bash
```
 $ file test.xlsb
 test.xlsb: Microsoft Excel 2007+
 $ unzip -l test.xlsb
 Archive:  test.xlsb
   Length      Date    Time    Name
 ---------  ---------- -----   ----
      1123  01-01-1980 00:00   [Content_Types].xml
       588  01-01-1980 00:00   _rels/.rels
       698  01-01-1980 00:00   xl/_rels/workbook.bin.rels
       500  01-01-1980 00:00   xl/workbook.bin
       824  01-01-1980 00:00   xl/styles.bin
      6995  01-01-1980 00:00   xl/theme/theme1.xml
       284  01-01-1980 00:00   xl/worksheets/_rels/sheet1.bin.rels
       133  01-01-1980 00:00   xl/sharedStrings.bin
    287030  01-01-1980 00:00   xl/worksheets/sheet1.bin
     13193  01-01-1980 00:00   xl/worksheets/binaryIndex1.bin
       614  01-01-1980 00:00   docProps/core.xml
       776  01-01-1980 00:00   docProps/app.xml
 ---------                     -------
    312758                     12 files
 
 $ unzip -l  test.xlsx
 Archive:  test.xlsx
   Length      Date    Time    Name
 ---------  ---------- -----   ----
       177  03-09-2022 08:55   docProps/app.xml
       555  03-09-2022 08:55   docProps/core.xml
     10140  03-09-2022 08:55   xl/theme/theme1.xml
    587445  03-09-2022 08:55   xl/worksheets/sheet1.xml
      3126  03-09-2022 08:55   xl/styles.xml
       531  03-09-2022 08:55   _rels/.rels
       547  03-09-2022 08:55   xl/workbook.xml
       504  03-09-2022 08:55   xl/_rels/workbook.xml.rels
       975  03-09-2022 08:55   [Content_Types].xml
 ---------                     -------
    604000                     9 files    
```

pandasのversion 1.0.0からは、内部でpyxlsb を利用して Excel Binary Workbook をロードできるようになっています。
次のように  `read_excel()` の引数に  `engine="pyxlsb"` を与えて読み込むだけです。


```
 In [2]: # %load c40_pyxlsb_pandas.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_excel("test.xlsb", engine="pyxlsb")
    ...:
    ...: # df
    ...:
 
 In [3]: df
 Out[3]:
        Date        High         Low  ...       Close    Volume   Adj Close
 0     42006   44.650002   42.652000  ...   43.862000  23822000   43.862000
 1     42009   43.299999   41.431999  ...   42.018002  26842500   42.018002
 2     42010   42.840000   40.841999  ...   42.256001  31309500   42.256001
 3     42011   42.956001   41.956001  ...   42.189999  14842000   42.189999
 4     42012   42.759998   42.001999  ...   42.124001  17212500   42.124001
 ...     ...         ...         ...  ...         ...       ...         ...
 1803  44622  886.479980  844.270020  ...  879.890015  24881100  879.890015
 1804  44623  886.440002  832.599976  ...  839.289978  20541200  839.289978
 1805  44624  855.650024  825.159973  ...  838.289978  22333200  838.289978
 1806  44627  866.140015  804.570007  ...  804.580017  24073300  804.580017
 1807  44628  849.989990  782.169983  ...  824.400024  26487200  824.400024
 
 [1808 rows x 7 columns]
 
 In [4]:
 
```

基本的には Pandas から利用するだけで十分ですが、pyxlsb を単独で使用する場合でも、使い方は単純です。次のコードは、 `test.xlsb` の先頭から10行はCSVファイルに変換するものです。


```
 In [2]: # %load c41_pyxlsb_csv.py
    ...: import csv
    ...: from pyxlsb import open_workbook
    ...:
    ...: with open_workbook('test.xlsb') as wb:
    ...:     for name in wb.sheets:
    ...:         with wb.get_sheet(name) as sheet, open(name + '.csv', 'w') as f:
    ...:
    ...:             writer = csv.writer(f)
    ...:             for num, row in enumerate(sheet.rows()):
    ...:                 if num <= 10:
    ...:                     wc = writer.writerow([c.v for c in row])
    ...:
 
 In [3]: !cat Sheet1.csv
 Date,High,Low,Open,Close,Volume,Adj Close
 42006.0,44.65000152587891,42.65200042724609,44.57400131225586,43.86199951171875,23822000.0,43.86199951171875
 42009.0,43.29999923706055,41.43199920654297,42.90999984741211,42.01800155639648,26842500.0,42.01800155639648
 42010.0,42.84000015258789,40.84199905395508,42.01200103759766,42.25600051879883,31309500.0,42.25600051879883
 42011.0,42.95600128173828,41.95600128173828,42.66999816894531,42.18999862670898,14842000.0,42.18999862670898
 42012.0,42.7599983215332,42.00199890136719,42.5620002746582,42.12400054931641,17212500.0,42.12400054931641
 42013.0,41.99599838256836,40.99200057983398,41.78400039672852,41.33200073242188,23341500.0,41.33200073242188
 42016.0,40.89400100708008,39.84999847412109,40.61000061035156,40.44200134277344,29751500.0,40.44200134277344
 42017.0,41.52199935913086,40.18199920654297,40.66400146484375,40.84999847412109,22386500.0,40.84999847412109
 42018.0,39.04000091552734,37.0,37.16600036621094,38.53799819946289,57759500.0,38.53799819946289
 42019.0,39.15000152587891,38.0,38.89799880981445,38.37400054931641,26082500.0,38.37400054931641
 
 In [4]:
 
```

## 参考資料
- Pandas
  - [オフィシャルサイト ](https://pandas.pydata.org/)
  - [公式ドキュメント ](https://pandas.pydata.org/docs/)
- OpenPyXL
  - [ソースコード ](https://foss.heptapod.net/openpyxl/openpyxl)
  - [公式ドキュメント ](https://openpyxl.readthedocs.io/en/latest/index.html#)
- pycal
- xlcalcurator
- xlwings
  - [オフィシャルサイト ](https://www.xlwings.org/)
  - [公式ドキュメント ](https://docs.xlwings.org/ja/latest/index.html)
- pyxlsb
  - [ソースコード ](https://github.com/willtrnr/pyxlsb)
- [Excel Formula Parsing ](https://ewbi.blogs.com/develops/2004/12/excel_formula_p.html) ー　Excelの数式を構文解釈してくれるサービス


#Excel


