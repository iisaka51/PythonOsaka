gspread-dataframeを使ってみよう
=================

![](https://gyazo.com/3d51d68e57347305f78735106914deb8.png)
## はじめに
この資料は、gspread-dataframe を使ってpandasの DataFrame とのデータ変換を説明するものです。gspread の使用方法については、"[PythonでGoogleSpreadsheetsを読み書きしてみよう]" を参照してください。

## gspread-dataframe について
[gspread-dataframe https://pypi.org/project/gspread-dataframe/] はGoogle Spreadsheets のワークシートとPandasのDataFrameとの間のデータフローを簡単に実現するものです。[gspread ](https://pypi.org/project/gspread)  ライブラリを使って取得できるすべてのワークシートは、簡単にDataFrame として取得することができます。

## インストール
gspread-dataframe は次のようにインストールすることができます。

 bash
```
 # Linux or MacOS
 $ pytohn -m pip install gspread-dataframe
 
 # Windows
 $ py -3 -m pip install gspread-dataframe
```

### 使用方法
次のようなサンプルのスプレッドシートを使って説明して行きます。


![](https://gyazo.com/f94b4cdd12526ae9fb7cac583a6aae2b.png)


このスプレッドシートをオープンする処理は次のようなものです。


```
 In [2]: # %load c01_open_worksheet.py
    ...: import os
    ...: import gspread
    ...: from pathlib import Path
    ...:
    ...: credential_dir = Path.home() / 'security'
    ...: keyfile = os.environ.get('PYTHONOSAKA_KEYFILE', default='credentials.jso
    ...: n')
    ...: credential_path = credential_dir / keyfile
    ...: sheetname= 'PythonOsaka_GSpread_Tutorial'
    ...:
    ...: gc = gspread.service_account(filename=credential_path)
    ...:
    ...: try:
    ...:     workbook = gc.open(sheetname)
    ...: except SpreadsheetNotFound:
    ...:     workbook = gc.create(sheetname)
    ...:     workbook.share('iisaka51@gmail.com', perm_type='user', role='owner')
    ...:
    ...:
    ...: worksheet = workbook.worksheet('シート2')
    ...:
 
 In [3]:
 
```


## ラッパーライブラリ
スプレッドシートを開く処理をモジュールにしておくと使い勝手がよくなりまうす。


```
 import os
 import gspread
 import pydantic
 from pathlib import Path
 
 class BaseSetting(pydantic.BaseSettings):
     class Config:
         env_prefix=''
         use_enum_values = True
 
 class GSpreadConfig(BaseSetting):
     GSPREAD_CREDENTIAL_PATH: Path = Path.home() / 'security/credentials.json'
     GSPREAD_DEFAULT_USER: pydantic.EmailStr = '__YOUR_GMAIL_ADDRESS__@gmail.com'
     GSPREAD_PERM_TYPE: str = 'user'
     GSPREAD_ROLE: str = 'owner'
 
 class GSpread(object):
 
     def __init__(self, filename='sample', sheetname='Sheet1', create=True):
         self.conf = GSpreadConfig()
         self.gc = gspread.service_account(
                      filename=self.conf.GSPREAD_CREDENTIAL_PATH)
         self.filename = filename
         self.sheetname = sheetname
         try:
             self.workbook = self.gc.open(self.filename)
         except gspread.SpreadsheetNotFound:
             self.workbook = self.gc.create(self.filename)
             self.workbook.share(
                 self.conf.GSPREAD_DEFAULT_USER,
                 perm_type=self.conf.GSPREAD_PERM_TYPE,
                 role=self.conf.GSPREAD_ROLE)
 
         try:
             self.worksheet = self.workbook.worksheet(self.sheetname)
         except:
             if create:
                 self.worksheet = self.workbook.add_worksheet(self.sheetname)
             else:
                 self.worksheet = self.workbook.sheet1
                 self.sheetname = self.worksheet.title
 
     @property
     def wb(self):
         return self.workbook
 
     @property
     def ws(self):
         return self.worksheet
                       
```

このラッパーライブライの使い方は次の通りです。


```
 In [2]: # %load c05_create_newfile.py
    ...: from gspread_utils import GSpread
    ...:
    ...: gs = GSpread('PythonOsaka_tempfile')
    ...:
    ...: # gs.worksheet
    ...:
 
 In [3]: gs.worksheet
 Out[3]: <Worksheet 'Sheet1' id:0>
 
 In [4]: gs.workbook
 Out[4]: <Spreadsheet 'PythonOsaka_tempfile' id:1wsiRIABIigjBhdsSU0AG0e-ddYHz6c43cbc_fzqTeqk>
 
 In [5]:
 
```


## ワークシートの内容をDataFrameに取り込む 

gspread では次のような処理になります。


```
 In [14]: # %load c02_convert_dataframe.py
     ...: import pandas as pd
     ...: from gspread_utils import GSpread
     ...:
     ...: ws = GSpread('PythonOsaka_GSpread_Tutorial', "シート2").worksheet
     ...:
     ...: data1 = ws.get_all_values()
     ...: df1 = pd.DataFrame(data1, columns=[0,1,2,3])
     ...:
     ...: data2 = ws.get_all_values(value_render_option='FORMULA')
     ...: df2 = pd.DataFrame(data2, columns=[0,1,2,3])
     ...:
     ...: v1 = f'{type(df1[0][0])}, {type(df1[1][0])}'
     ...: v2 = f'{type(df2[0][0])}, {type(df2[1][0])}'
     ...:
     ...: # df1
     ...: # df2
     ...:
 
 In [15]: df1
 Out[15]:
              0    1    2    3
 0   2022/01/01   10  120  130
 1   2022/02/01   20  110  130
 2   2022/03/01   30  100  130
 3   2022/04/01   40   90  130
 4   2022/05/01   50   80  130
 5   2022/06/01   60   70  130
 6   2022/07/01   70   60  130
 7   2022/08/01   80   50  130
 8   2022/09/01   90   40  130
 9   2022/10/01  100   30  130
 10  2022/11/01  110   20  130
 11  2022/12/01  120   10  130
 
 In [16]: df2
 Out[16]:
         0    1    2              3
 0   44562   10  120    =SUM(B1:C1)
 1   44593   20  110    =SUM(B2:C2)
 2   44621   30  100    =SUM(B3:C3)
 3   44652   40   90    =SUM(B4:C4)
 4   44682   50   80    =SUM(B5:C5)
 5   44713   60   70    =SUM(B6:C6)
 6   44743   70   60    =SUM(B7:C7)
 7   44774   80   50    =SUM(B8:C8)
 8   44805   90   40    =SUM(B9:C9)
 9   44835  100   30  =SUM(B10:C10)
 10  44866  110   20  =SUM(B11:C11)
 11  44896  120   10  =SUM(B12:C12)
 
 In [17]:
 
```

一見するとこれでよいように見えますが、日付のカラムを含めすべてを文字列となってしまっています。


```
 In [5]: df1.dtypes
 Out[5]:
 0    object
 1    object
 2    object
 3    object
 dtype: object
 
 In [6]: df2.dtypes
 Out[6]:
 0     int64
 1     int64
 2     int64
 3    object
 dtype: object
 
 In [7]: v1
 Out[7]: "<class 'str'>, <class 'str'>"
 
 In [8]: v2
 Out[8]: "<class 'numpy.int64'>, <class 'numpy.int64'>"
 
 In [9]:
```

通常は次のように型を指定を適用させることになります。


```
 In [2]: # %load c03_convert_dataframe_dtype.py
    ...: import pandas as pd
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread('PythonOsaka_GSpread_Tutorial', "シート2").worksheet
    ...:
    ...: all_rows = ws.get_all_values()
    ...: df = pd.DataFrame(all_rows, columns=[0,1,2,3])
    ...:
    ...: df[[0]] = df[[0]].apply(pd.to_datetime)
    ...: df[[1,2,3]] = df[[1,2,3]].apply(pd.to_numeric)
    ...:
    ...: # df
    ...: # df.dtypes
    ...:
 
 In [3]: df
 Out[3]:
             0    1    2    3
 0  2022-01-01   10  120  130
 1  2022-02-01   20  110  130
 2  2022-03-01   30  100  130
 3  2022-04-01   40   90  130
 4  2022-05-01   50   80  130
 5  2022-06-01   60   70  130
 6  2022-07-01   70   60  130
 7  2022-08-01   80   50  130
 8  2022-09-01   90   40  130
 9  2022-10-01  100   30  130
 10 2022-11-01  110   20  130
 11 2022-12-01  120   10  130
 
 In [4]: df.dtypes
 Out[4]:
 0    datetime64[ns]
 1             int64
 2             int64
 3             int64
 dtype: object
 
 In [5]:
 
```

こんどは、gspread-dataframe を使って処理してみましょう。 `get_as_dataframe()` にWorksheetオブジェクトを与えます。


```
 In [2]: # %load c04_read_as_dataframe.py
    ...: import gspread_dataframe as gd
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread('PythonOsaka_GSpread_Tutorial', "シート2").worksheet
    ...:
    ...: df1 = gd.get_as_dataframe(ws,
    ...:               dtype={0: str, 1:int, 2:int, 3:str},
    ...:               parse_dates=[0], header=None, evaluate_formulas=True,
    ...:               nrows=12, usecols=[0,1,2,3])
    ...:
    ...: df2 = gd.get_as_dataframe(ws,
    ...:               dtype={0: str, 1:int, 2:int, 3:str},
    ...:               parse_dates=[0], header=None,
    ...:               nrows=12, usecols=[0,1,2,3])
    ...:
    ...: v1 = f'{type(df1[0][0])}, {type(df1[1][0])}'
    ...: v2 = f'{type(df2[0][0])}, {type(df2[1][0])}'
    ...:
 
 In [3]: df1
 Out[3]:
             0    1    2    3
 0  2022-01-01   10  120  130
 1  2022-02-01   20  110  130
 2  2022-03-01   30  100  130
 3  2022-04-01   40   90  130
 4  2022-05-01   50   80  130
 5  2022-06-01   60   70  130
 6  2022-07-01   70   60  130
 7  2022-08-01   80   50  130
 8  2022-09-01   90   40  130
 9  2022-10-01  100   30  130
 10 2022-11-01  110   20  130
 11 2022-12-01  120   10  130
 
 In [4]: df2
 Out[4]:
             0    1    2              3
 0  2022-01-01   10  120    =SUM(B1:C1)
 1  2022-02-01   20  110    =SUM(B2:C2)
 2  2022-03-01   30  100    =SUM(B3:C3)
 3  2022-04-01   40   90    =SUM(B4:C4)
 4  2022-05-01   50   80    =SUM(B5:C5)
 5  2022-06-01   60   70    =SUM(B6:C6)
 6  2022-07-01   70   60    =SUM(B7:C7)
 7  2022-08-01   80   50    =SUM(B8:C8)
 8  2022-09-01   90   40    =SUM(B9:C9)
 9  2022-10-01  100   30  =SUM(B10:C10)
 10 2022-11-01  110   20  =SUM(B11:C11)
 11 2022-12-01  120   10  =SUM(B12:C12)
 
 In [5]: v1
 Out[5]: "<class 'pandas._libs.tslibs.timestamps.Timestamp'>, <class 'numpy.int64'>"
 
 In [6]: v2
 Out[6]: "<class 'pandas._libs.tslibs.timestamps.Timestamp'>, <class 'numpy.int64'>"
 
 In [7]:
 
```

一度の呼び出しで型の設定まで行うことができます。

ここで、注意することはもとのスプレッドシートは空のセルが多数含まれていることです。


```
 In [9]: max_rows = len(ws.get_all_values())
 
 In [10]: max_rows
 Out[10]: 12
 
 In [11]: ws.row_count
 Out[11]: 1000
 
 In [12]: ws.col_count
 Out[12]: 24
 
 In [13]:
 
```

そのため  `nrows` および  `use_cols` を指定しないとワークシート全体を読み込んで欠損値( `NaN` )を含んだ状態のDataFrameオブジェクトが返されることに注意してください。


```
 In [13]: df0 = gd.get_as_dataframe(ws)
 
 In [14]: df0
 Out[14]:
      2022/01/01    10    120  ... Unnamed: 21  Unnamed: 22  Unnamed: 23
 0    2022/02/01  20.0  110.0  ...         NaN          NaN          NaN
 1    2022/03/01  30.0  100.0  ...         NaN          NaN          NaN
 2    2022/04/01  40.0   90.0  ...         NaN          NaN          NaN
 3    2022/05/01  50.0   80.0  ...         NaN          NaN          NaN
 4    2022/06/01  60.0   70.0  ...         NaN          NaN          NaN
 ..          ...   ...    ...  ...         ...          ...          ...
 994         NaN   NaN    NaN  ...         NaN          NaN          NaN
 995         NaN   NaN    NaN  ...         NaN          NaN          NaN
 996         NaN   NaN    NaN  ...         NaN          NaN          NaN
 997         NaN   NaN    NaN  ...         NaN          NaN          NaN
 998         NaN   NaN    NaN  ...         NaN          NaN          NaN
 
 [999 rows x 24 columns]
 
 In [15]:
```


欠損値( `NaN` )は float のサブクラスとなっているため、 `dtype` を指定したときに、 `ValueError` の例外が発生することがあります。


```
 ValueError: Unable to convert column 1 to type int64
 
```

 `get_as_dataframe()` は　Pandas の TextParser をサポートしています。[pandas.read_csv() ](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)も同様にTextParser をサポートしているヘルパー関数なので、同じ引数を使用することができます。


## サンプルデータを用意

次のようなサンプルのCSVファイルを用意します。

 GAFAM.csv
```
 Name,Ticker
 Alphabet,GOOGL
 Apple,AAPL
 Meta,FB
 Amazon,AMZN
 Microsoft,MSFT
```

これを読み込んで DataFrame にするコードは次のものです。


```
 In [2]: # %load c06_read_csv.py
    ...: import pandas as pd
    ...:
    ...: gafam = pd.read_csv('GAFAM.csv')
    ...:
 
 In [3]: gafam
 Out[3]:
         Name Ticker
 0   Alphabet  GOOGL
 1      Apple   AAPL
 2       Meta     FB
 3     Amazon   AMZN
 4  Microsoft   MSFT
 
 In [4]:
 
```

## DataFrame の内容をワークシートに書き込む

まずは、このDataFrame を　gspread でスプレッドシートに書き込んでみます。


```
 In [2]: # %load c07_gspread_dataframe_to_sheet.py
    ...: import pandas as pd
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread('PythonOsaka_tempfile').worksheet
    ...:
    ...: _ = ws.clear()
    ...:
    ...: df = pd.read_csv('GAFAM.csv')
    ...: _ = ws.update(
    ...:         [df.columns.values.tolist()] + df.values.tolist())
    ...:
 
 In [3]:
 
```


![](https://gyazo.com/d7fe1ffce94097b9d75237f011b5deee.png)
gspread の　 `updae()` メソッドを使いました。これは、行のデータを要素とするリストを渡します。

今度は、gspread-dataframe で処理してみましょう。
 `set_with_dataframe()` にWorksheetオブジェクトと DataFrameオブジェクトを渡すだけです。こちらの方がシンプルですよね。


```
 In [2]: # %load c08_dataframe_to_sheet.py
    ...: import pandas as pd
    ...: from gspread_utils import GSpread
    ...: import gspread_dataframe as gd
    ...:
    ...: ws = GSpread('PythonOsaka_tempfile').worksheet
    ...: _ = ws.clear()
    ...:
    ...: df = pd.read_csv('GAFAM.csv')
    ...: gd.set_with_dataframe(ws, df)
    ...:
 
 In [3]:
 
```

この例では、セルA1から上書きをします。

書き出す位置を指定してみましょう。まず gspread では、 `update()` にセルを指示します。


```
 In [2]: # %load c09_gspread_dataframe_to_sheet_with_cordinate.py
    ...: import pandas as pd
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread('PythonOsaka_tempfile').worksheet
    ...:
    ...: _ = ws.clear()
    ...:
    ...: df = pd.read_csv('GAFAM.csv')
    ...: _ = ws.update( 'B2',
    ...:         [df.columns.values.tolist()] + df.values.tolist())
    ...:
 
 In [3]:
 
```

gsread-dataframe の  `set_with_dataframe()` では、 `row` と　 `col` で座標を指示します。


```
 In [2]: # %load c09_dataframe_to_sheet_specified_cordinate.py
    ...: import pandas as pd
    ...: from gspread_utils import GSpread
    ...: import gspread_dataframe as gd
    ...:
    ...: ws = GSpread('PythonOsaka_tempfile').worksheet
    ...: _ = ws.clear()
    ...:
    ...: df = pd.read_csv('GAFAM.csv')
    ...: gd.set_with_dataframe(ws, df, row=2, col=2)
    ...:
 
 In [3]:
 
```

![](https://gyazo.com/f81cafd9c681fff8136ff5127c73a15f.png)

## gspread-fornatting
gsread-dataframe の作者は gspreaed-formatting も開発していて、これを使うとテーブルでのヘッダのフォーマットが簡単に実現できてしまいます。


```
 In [2]: # %load c11_with_gsread_formatting.py
    ...: import pandas as pd
    ...: from gspread_utils import GSpread
    ...: import gspread_dataframe as gd
    ...: from gspread_formatting.dataframe import format_with_dataframe
    ...:
    ...: ws = GSpread('PythonOsaka_tempfile').worksheet
    ...: _ = ws.clear()
    ...:
    ...: df = pd.read_csv('GAFAM.csv')
    ...: gd.set_with_dataframe(ws, df, row=2, col=2)
    ...: _ = format_with_dataframe(ws, df, include_column_header=True)
    ...:
 
 In [3]:
 
```

![](https://gyazo.com/873fa5473f6986d6075a996f198abdb0.png)
書式については、Worksheetオブジェクトの `clear()` メソッドでクリアできないことに注意してください。


## 参考
- gspread-dataframe
  - [PyPI - gspread-dataframe ](https://pypi.org/project/gspread-dataframe/)
  - [ソースコード　](https://github.com/robin900/gspread-dataframe.git)
  - [公式ドキュメント ](https://pythonhosted.org/gspread-dataframe/)










