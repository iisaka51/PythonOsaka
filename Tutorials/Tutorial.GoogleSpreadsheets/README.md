PythonでGoogleSpreadsheetsを読み書きしてみよう
=================
![](https://gyazo.com/d74bc5963383c121e414c185be57fa09.png)


## はじめに
この資料では、PythonでGoogle Sheets APIを使用する方法について説明しています。
これを実現するパッケージには次のものがあります。

  - [gspread ](https://pypi.org/project/gspread/)
  - [gsheets ](https://pypi.org/project/gsheets/)
  - [EZSheets ](https://pypi.org/project/EZSheets/)
  - [pygsheets ](https://pypi.org/project/pygsheets/)

ここでは、gspread について説明してゆきます。

## gspread について
[gspread ](https://pypi.org/project/gspread/)　は　Google Spreadsheets にアクセスするための拡張ライブラリです。
次のような機能があります。

  - Google Sheets API v4に対応
  - タイトル、キー、URLでスプレッドシートをオープン
  - セル範囲を指定しての読み書き、および書式設定
  - 共有とアクセス制御
  - 更新のバッチ処理

Pythonスクリプトでスプレッドシートにアクセスし修正するのはとても簡単です。Google Sheetsはかなり強力で、Webアプリケーションのデータを保存するためのバックエンドストレージとしても利用することができます。

## 準備
まず、大前提として Googleアカウントを持っている必要があります。
その上で、[Google Developer Console ](https://console.developers.google.com) にアクセスして以下の設定を行います。

1. プロジェクトを（必要に応じて作成）を開く
![](https://gyazo.com/54286b30115e7b45f6378d028f40f7ab.png)

![](https://gyazo.com/7b74bd95b794477798b1cc58a3deaf50.png)
[! 新しいプロジェクト]　をクリックしてプロジェクトを作成します。
プロジェクトは最大10まで作成できます。

![](https://gyazo.com/5c09bdc4869651faa7b3a9b6204254b4.png)

  - サイドメニュー[! 有効なAPIとサービス]をクリック
![](https://gyazo.com/0db96e240a89875fdb34f89232e81132.png)

  - [! +APIとサービスを有効化]をクリック
![](https://gyazo.com/222a95e96da323d58825369c0c46ce91.png)

  - 次のAPIを検索して有効化
      -  `Drive Activity API`
      -  `Google Sheets API`

2. サイドメニュー[! 認証情報]をクリック

![](https://gyazo.com/69e6d7b3fc3cd9b8447d5a4117b7bb2a.png)
初回は次のダイアローグが表示されますが、ここは[! 認証情報を作成] をクリック

![](https://gyazo.com/987a5b6a2e02d4ccf8781968c646ec7e.png)



  - [! 同意画面を構成]をクリック
      - User Type を設定: [# 外部] を選択して[! 作成]をクリック
          - Google Workspace ユーザであれば[# 内部]を選択可能
    - [# アプリ情報画面] のフォームを入力
        - アプリ名:  任意の文字列
        - ユーザーサポートメール: 自分のメールアドレスを選択
        - デベロッパーの連絡先情報: 自分のメールアドレスを入力
        - [! 保存して次へ]をクリック

    - [# スコープ]は空欄のまま
        - [! 保存して次へ]をクリック

    - [# テストユーザ] で[! ＋ADD USERS]をクリック
        - 自分のメールアドレスを入力して[! 追加]をクリック
        - [! 保存して次へ]をクリック

        - [! ダッシュボードに戻る]をクリック

3. [! +認証情報を作成]をクリックして[# サービスアカウント]を選択

![](https://gyazo.com/15ad77377b60d25beab3e9c0de3e8618.png)

    - 表示されるフォームに以下を入力
        - サービスアカウント名： 任意の文字列
        - サービスアカウント名ID： デフォルトでサービスアカウント名が設定されます
        - サービスアカウントの説明：任意

![](https://gyazo.com/a416e5c69210d950870daf70738285e6.png)


        - [! 作成して続行] をクリック
        - [! ロール] を[# 編集者] に設定　　

![](https://gyazo.com/b3c1183ea003ab7079514c20aacf4799.png)

![](https://gyazo.com/8f169bdf424c89094a92fce65bd80b0f.png)

        - [! 完了] をクリック


4. サービスアカウント
    - 右側にある[! 操作]から[# 鍵の管理]を選択
![](https://gyazo.com/560e7167039d4c406482cec256e3c302.png)


    - [! 鍵を追加] をクリック[# 新しい鍵を作成] を選択
![](https://gyazo.com/c822a3bc268e11fbc71d464fcc2b7a52.png)


    - キータイプは [# JSON] を選択して[! 作成] をクリックすると...
![](https://gyazo.com/57732a0f52c292381b6f49f0d3063c9e.png)

    - JSONファイルがダウンロードされます。(必要に応じてファイル名を設定）
このJSONファイルは大事なので漏洩しないように注意してくだdさい。

既存のスプレッドシートをPythonからアクセスしたい場合は、このJSONに含まれる  `client_email` を　[# 編集者] 権限で共有します。この手順に従っていれば　 `サービスアカウントID@サービスアカウント名.iam.gserviceaccount.com` となっているはずです。


## インストール

gspread は次のようにインストールします。

 bash
```
 # Linux or MacOS
 $ python -m pip install gspread

 # Windows
 $ py -3 -m pip install gspread
```


![](https://gyazo.com/fd19282ef0c1a18c4a28655bbe485b5c.png)

## ワークシートを新規作成/削除
 `create()` メソッドで新規にワークシートを作成することができます。サービスアカウントを使用して作成したワークシートは、そのアカウントにのみ表示されます。Google Sheets で新しく作成したスプレッドシートに自分の Google アカウントでアクセスするには、共有するメールアドレスを登録する必要があります。共有するとドライブに表示されます。



```
 In [2]: # %load c00_create_worksheet.py
    ...: import os
    ...: import gspread
    ...: from pathlib import Path
    ...:
    ...: credential_dir = Path.home() / 'security'
    ...: keyfile = os.environ.get('PYTHONOSAKA_KEYFILE', default='credentials.jso
    ...: n')
    ...: credential_path = credential_dir / keyfile
    ...: sheetname= 'PythonOsaka_tempsheet'
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
    ...: worksheet = workbook.sheet1
    ...:

 In [3]:

```

このコードを実行すると、Google Drive の共有アイテムに `PythonOsaka_tempsheet` が作成されます。
オーナーは共有設定を変更することができます。あなたがオーナーのアイテムは、あなたのストレージを使用します。

 `create()` メソッドを複数回実行すると同じファイル名のスプレッドシートが複数作成されるので注意してください。
指定したスプレッドシートが存在しないときに `open()` すると、サービスアカウントのユーザがオーナーとなるファイルが作成されます。 `share()` で自分のアカウントと共有するようにします。 `share()` を実行するたびにメールが届きます。

削除できる権限が与えられていれば、 `gc_del_spreadsheet(sheetname)` でワークシートを削除することができます。

## ワークシートをオープン
Google Developer Console　で作成したサービスアカウントのJSONファイルへのパスを環境変数に設定しておきます。

 bash
```
 $ ls $HOME/security


 $ export PYTHONOSAKA_KEYFILE=$HOME/security/pythonosaka-c3e7b4957795.json

```

これはGoogle Spreadsheets にアクセスするコードを Giyhub などで管理するようなときに非常に重要です。秘密鍵をGithubレポジトリで公開してしまうことを防いでくれます。


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
次のようなラッパーライブラリを用意すると、gspread をもっと手軽に利用できるようになります。

 gspread_utils.py
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

使い方は次のようになります。前述の例で環境変数  `PYTHONOSAKA_KEYFILE` としていましたが、このラッパーライブラリでは、 `GSPREAD_CREDENTIAL_PATH` にJSONファイルへのパスを設定します。デフォルトは、 `$HOME/secuirty/credentials.json` です。
 `GSPREAD_DEFAULT_USER` に使用するGoogleアカウントのメールアドレスを設定します。
これらは、環境変数で設定することもできます。


```
 In [2]: # %load c91_create_newfile.py
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

## ワークシートを選択

 `worksheets()` メソッドは worksheet オブジェクトをリストで返します。
 `.sheet1` 属性は先頭のワークシートがアサインされています。
 `.worksheet()` にシート名を与えるとそのシートのworksheet オブジェクト返します。


```
 In [2]: # %load c01_select_sheet.py
    ...: from gspread_utils import GSpread
    ...:
    ...: gs = GSpread("PythonOsaka_GSpread_Tutorial")
    ...:
    ...: v1 = gs.workbook.sheet1
    ...: v2 = gs.workbook.worksheets()
    ...: v3 = gs.workbook.worksheet("シート2")
    ...:
    ...: gs = GSpread("PythonOsaka_GSpread_Tutorial", "シート2")
    ...: v4 = gs.worksheet
    ...:

 In [3]: v1
 Out[3]: <Worksheet 'シート1' id:0>

 In [4]: v2
 Out[4]: [<Worksheet 'シート1' id:0>, <Worksheet 'シート2' id:2103255368>]

 In [5]: v3
 Out[5]: <Worksheet 'シート2' id:2103255368>

 In [6]: v4
 Out[6]: <Worksheet 'シート2' id:2103255368>

 In [7]:

```

## ワークシートから全レコードを取得
レコードまたはセルの値を取得するには、次のメソッドのどちらかで行います。

  -  `get_all_values()` ー　ワークシートからすべての値をリストのリストとして取得します。
  -  `get_all_records()` ー　ワークシートからすべての値を辞書のリストとして取得します。

ワークシートのセルに数式がある場合は、Gooogle Spreadsheets で計算された結果が返されます。


```
 In [2]: # %load c02_get_all_values.py
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: v1 = ws.get_all_values()
    ...: v2 = ws.get_all_records()
    ...:
    ...: # v1
    ...: # v2
    ...:

 In [3]: v1
 Out[3]:
 [['2022/01/01', '10', '120', '130'],
  ['2022/02/01', '20', '110', '130'],
  ['2022/03/01', '30', '100', '130'],
  ['2022/04/01', '40', '90', '130'],
  ['2022/05/01', '50', '80', '130'],
  ['2022/06/01', '60', '70', '130'],
  ['2022/07/01', '70', '60', '130'],
  ['2022/08/01', '80', '50', '130'],
  ['2022/09/01', '90', '40', '130'],
  ['2022/10/01', '100', '30', '130'],
  ['2022/11/01', '110', '20', '130'],
  ['2022/12/01', '120', '10', '130']]

 In [4]: v2
 Out[4]:
 [{'2022/01/01': '2022/02/01', '10': 20, '120': 110, '130': 130},
  {'2022/01/01': '2022/03/01', '10': 30, '120': 100, '130': 130},
  {'2022/01/01': '2022/04/01', '10': 40, '120': 90, '130': 130},
  {'2022/01/01': '2022/05/01', '10': 50, '120': 80, '130': 130},
  {'2022/01/01': '2022/06/01', '10': 60, '120': 70, '130': 130},
  {'2022/01/01': '2022/07/01', '10': 70, '120': 60, '130': 130},
  {'2022/01/01': '2022/08/01', '10': 80, '120': 50, '130': 130},
  {'2022/01/01': '2022/09/01', '10': 90, '120': 40, '130': 130},
  {'2022/01/01': '2022/10/01', '10': 100, '120': 30, '130': 130},
  {'2022/01/01': '2022/11/01', '10': 110, '120': 20, '130': 130},
  {'2022/01/01': '2022/12/01', '10': 120, '120': 10, '130': 130}]

 In [5]:

```


 `row_values()` 、 `col_values()` は、与えた行番号、列番号のセルの内湯をリストで返します。


```
 In [2]: # %load c03_row_col_values.py
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: v1 = ws.row_values(1)
    ...: v2 = ws.col_values(1)
    ...:
    ...: # v1
    ...: # v2
    ...:

 In [3]: v1
 Out[3]: ['2022/01/01', '10', '120', '130']

 In [4]: v2
 Out[4]:
 ['2022/01/01',
  '2022/02/01',
  '2022/03/01',
  '2022/04/01',
  '2022/05/01',
  '2022/06/01',
  '2022/07/01',
  '2022/08/01',
  '2022/09/01',
  '2022/10/01',
  '2022/11/01',
  '2022/12/01']

 In [5]:

```


## DataFrame に変換
次のようにすると、読み込んだデータをDataFrameに変換することができます。


```
 In [2]: # %load c04_read_as_dataframe.py
    ...: import pandas as pd
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: all_rows = ws.get_all_values()
    ...: columns = all_rows.pop(0)
    ...: df = pd.DataFrame(all_rows, columns=columns)
    ...:
    ...: new_columns = list(df.columns.values.tolist())
    ...: values = df.values.tolist()
    ...:
    ...: # to Google Spreadsheets
    ...: # ws.update(new_columns + values)
    ...:

 In [3]: df
 Out[3]:
     2022/01/01   10  120  130
 0   2022/02/01   20  110  130
 1   2022/03/01   30  100  130
 2   2022/04/01   40   90  130
 3   2022/05/01   50   80  130
 4   2022/06/01   60   70  130
 5   2022/07/01   70   60  130
 6   2022/08/01   80   50  130
 7   2022/09/01   90   40  130
 8   2022/10/01  100   30  130
 9   2022/11/01  110   20  130
 10  2022/12/01  120   10  130

 In [4]:

```

詳しくは後述していますが、 `update()` メソッドでDataFrameの内容をGoogle Spreadsheets  へ書き込みこともできます。

## Numpy Arrayに変換
NumPy は Python で科学計算を行うためのライブラリで、高性能な多次元配列を扱うためのツールを提供しています。Google Spreadsheets のシートの内容をNumPyの配列に読み込むためには、次のようにコードします。


```
 In [2]: # %load c05_read_as_numpy_array.py
    ...: import numpy as np
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: array = np.array(ws.get_all_values())
    ...:
    ...: array2 = np.array([[1, 2, 3], [4, 5, 6]])
    ...: # ws.update('F1', array2.tolist())
    ...:

 In [3]: array
 Out[3]:
 array([['2022/01/01', '10', '120', '130'],
        ['2022/02/01', '20', '110', '130'],
        ['2022/03/01', '30', '100', '130'],
        ['2022/04/01', '40', '90', '130'],
        ['2022/05/01', '50', '80', '130'],
        ['2022/06/01', '60', '70', '130'],
        ['2022/07/01', '70', '60', '130'],
        ['2022/08/01', '80', '50', '130'],
        ['2022/09/01', '90', '40', '130'],
        ['2022/10/01', '100', '30', '130'],
        ['2022/11/01', '110', '20', '130'],
        ['2022/12/01', '120', '10', '130']], dtype='<U10')

 In [4]:

```

詳しくは後述していますが、 `update()` メソッドでNumPy Array のデータを Google Spreadsheets へ書き込みことができます。
この例の場合、セルF1を始点として2行3列にデータが書き込まれます。

![](https://gyazo.com/9dd4ce1590241dec3e622747051f8c8d.png)


## セルをクリア
先の例で セル `F1:H2` にデータが書き込まれたのでこれをクリアしましょう。


```
 In [2]: # %load c06_clear.py
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: _ = ws.batch_clear(["F1:H2"])
    ...:
    ...: # ワークシート全体をクリアするときは
    ...: # _ = ws.clear()
    ...:
    ...:

 In [3]:

```

 `batch_clear()` メソッドに削除したいセルのリストを与えます。ワークシート全体をクリアしたい場合は、 `clear()` メソッドを呼び出します。

## ワークシートからセルの値を取得
特定のセルの値を取得するには、 `acell()` メソッドを使用します。 `acell()` に領域を与えることもできますが、返される値は1つだけです。複数の値が欲しい場合は、 `get_values()` メソッドを使用します。指定したセルの値がリストとして返されます。
 `range()` メソッドは与えた領域に該当するセルのCellオブジェクトをリストとして返します。


```
 In [2]: # %load c07_acell.py
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: v1 = ws.acell('A3').value
    ...: v2 = ws.acell('A3:A4').value
    ...: v3 = ws.get_values('A3')
    ...: v4 = ws.get_values('A3:A4')
    ...: v5 = ws.range('A3:A4')
    ...: v6 = [c.value for c in v5]
    ...:

 In [3]: v1
 Out[3]: '2022/03/01'

 In [4]: v2
 Out[4]: '2022/03/01'

 In [5]: v3
 Out[5]: [['2022/03/01']]

 In [6]: v4
 Out[6]: [['2022/03/01'], ['2022/04/01']]

 In [7]: v5
 Out[7]: [<Cell R3C1 '2022/03/01'>, <Cell R4C1 '2022/04/01'>]

 In [8]: v6
 Out[8]: ['2022/03/01', '2022/04/01']

 In [9]:

```

座標で値を取得するためには `cell()` メソッドを使用します。次の例では、 `'2022/03/01'` が取得されます。


```
 In [2]: # %load c08_cell.py
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: data =  ws.cell(3,1).value
    ...:
    ...: # data
    ...:

 In [3]: data
 Out[3]: '2022/03/01'

 In [4]:

```

 `cell(row=3, cell=1)` と呼び出すこともできます。 `row` と `cell` はそれぞれ1で始まります。

## 複数のセルから一括して値を取得
 `batch_get()` メソッドを使用すると、リストで指定した複数のセルの値を一括して取得することができます。


```
 In [2]: # %load c09_batch_get.py
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: all_rows = ws.get_all_values()
    ...: data =  ws.batch_get(['A1:A12', 'D1:D12'])
    ...:
    ...: # data
    ...:

 In [3]: data
 Out[3]:
 [[['2022/01/01'],
   ['2022/02/01'],
   ['2022/03/01'],
   ['2022/04/01'],
   ['2022/05/01'],
   ['2022/06/01'],
   ['2022/07/01'],
   ['2022/08/01'],
   ['2022/09/01'],
   ['2022/10/01'],
   ['2022/11/01'],
   ['2022/12/01']],
  [['130'],
   ['130'],
   ['130'],
   ['130'],
   ['130'],
   ['130'],
   ['130'],
   ['130'],
   ['130'],
   ['130'],
   ['130'],
   ['130']]]

 In [4]:

```

## ワークシートの追加/コピー/削除
 `add_worksheet()` メソッドを使用すると、同じスプレッドシートに別のシートを作成します。
 `del_worksheet()` メソッド は与えたworkseetオブジェクトのワークシートを削除します。
 `duplicate_sheet()` メソッドは与えた worksheet オブジェクトのコピーを作成します。


```
 In [2]: # %load c10_add_worksheet.py
    ...: from gspread_utils import GSpread
    ...:
    ...: gs = GSpread("PythonOsaka_GSpread_Tutorial", "シート2")
    ...:
    ...: ws1 = gs.workbook.duplicate_sheet(gs.worksheet.id,
    ...:              insert_sheet_index=2, new_sheet_name='Sheet3')
    ...: ws2 = gs.workbook.add_worksheet(title="Finance", rows="10", cols="10")
    ...: # _ = gs.workbook.del_worksheet(ws1)
    ...: # _ = gs.workbook.del_worksheet(ws2)
    ...:

 In [3]: ws1
 Out[3]: <Worksheet 'Sheet3' id:184257767>

 In [4]: ws2
 Out[4]: <Worksheet 'Finance' id:816103225>

 In [5]: ws2.row_count
 Out[5]: 10

 In [6]: ws2.col_count
 Out[6]: 10

 In [7]:

```

この結果、Google Spreadsheets で、 `Sheet3` と 10行10列のシート名  `Finance` が作成されます。

![](https://gyazo.com/5d7a8f8f1339b1d748636abb680b41e0.png)


 `add_worksheet()` を呼び出した時、指定したタイトル のワークシートが既に存在していると、  `APIError` の例外が発生します。


```
 APIError: {'code': 400, 'message': 'Invalid requests[0].addSheet: A sheet with the name "Finance" already exists. Please enter another name.', 'status': 'INVALID_ARGUMENT'}

```

 `del_worksheet()` を呼び出したときに、該当するワークシートが存在していないときは、 `APIError` の例外が発生します。


```
 APIError: {'code': 400, 'message': 'Invalid requests[0].deleteSheet: No sheet with id: 21686688', 'status': 'INVALID_ARGUMENT'}


```

## セルの値を更新する
 `update()` メソッドを使用するとセルの値を更新することができます。


```
 In [2]: # %load c11_update.py
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: prev_d1 =  ws.acell('D1').value
    ...: cell_c1 =  ws.update('C1', 200)
    ...: cell_d1 =  ws.acell('D1').value
    ...:
    ...: # prev_d1
    ...: # cell_c1
    ...: # cell_d1
    ...:

 In [3]: prev_d1
 Out[3]: '130'

 In [4]: cell_c1
 Out[4]:
 {'spreadsheetId': '1gsv8InBWxV89POd4z7pY3af1pJO1ADGOmfdO5ql2DOo',
  'updatedRange': "'シート2'!C1",
  'updatedRows': 1,
  'updatedColumns': 1,
  'updatedCells': 1}

 In [5]: cell_d1
 Out[5]: '210'

 In [6]:

```

ここで注目してほしいことは、もとのワークシートのセルD1には、 `=SUM(B1:C1)` という数式が入っていて、セルC1への更新は、セルD1に反映されていることです。

座標を使用して同じ操作を行うことができます。


```
 In [2]: # %load c12_update_cell.py
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: prev_d1 =  ws.acell('D1').value
    ...: cell_c1 =  ws.update_cell(1,3, 120)
    ...: cell_d1 =  ws.acell('D1').value
    ...:
    ...: # prev_d1
    ...: # cell_c1
    ...: # cell_d1
    ...:

 In [3]: prev_d1
 Out[3]: '210'

 In [4]: cell_c1
 Out[4]:
 {'spreadsheetId': '1gsv8InBWxV89POd4z7pY3af1pJO1ADGOmfdO5ql2DOo',
  'updatedRange': "'シート2'!C1",
  'updatedRows': 1,
  'updatedColumns': 1,
  'updatedCells': 1}

 In [5]: cell_d1
 Out[5]: '130'

 In [6]:

```

## 複数のセルを一括して更新
 `uppdate_cells()` 　を使用すると複数の座標のセルを一度に更新することができます。


```
 In [2]: # %load c13_update_cells.py
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: prev_data = ws.get_all_values()
    ...:
    ...: cell_list = ws.range('E1:E12')
    ...: for cell in cell_list:
    ...:     cell.value = 300
    ...:
    ...: _ = ws.update_cells(cell_list)
    ...:
    ...: data = ws.get_all_values()
    ...:
    ...: # prev_data
    ...: # data
    ...:

 In [3]: prev_data
 Out[3]:
 [['2022/01/01', '10', '120', '130'],
  ['2022/02/01', '20', '110', '130'],
  ['2022/03/01', '30', '100', '130'],
  ['2022/04/01', '40', '90', '130'],
  ['2022/05/01', '50', '80', '130'],
  ['2022/06/01', '60', '70', '130'],
  ['2022/07/01', '70', '60', '130'],
  ['2022/08/01', '80', '50', '130'],
  ['2022/09/01', '90', '40', '130'],
  ['2022/10/01', '100', '30', '130'],
  ['2022/11/01', '110', '20', '130'],
  ['2022/12/01', '120', '10', '130']]

 In [4]: data
 Out[4]:
 [['2022/01/01', '10', '120', '130', '300'],
  ['2022/02/01', '20', '110', '130', '300'],
  ['2022/03/01', '30', '100', '130', '300'],
  ['2022/04/01', '40', '90', '130', '300'],
  ['2022/05/01', '50', '80', '130', '300'],
  ['2022/06/01', '60', '70', '130', '300'],
  ['2022/07/01', '70', '60', '130', '300'],
  ['2022/08/01', '80', '50', '130', '300'],
  ['2022/09/01', '90', '40', '130', '300'],
  ['2022/10/01', '100', '30', '130', '300'],
  ['2022/11/01', '110', '20', '130', '300'],
  ['2022/12/01', '120', '10', '130', '300']]

 In [5]:

```

 `range()` メソッドで指定した範囲の Cellオブジェクトを生成し、そこに値をセットしたあと、 `batch_cells()` で一括して更新するわけです。

## セルの検索
 `find()` メソッドに検索したい内容を与えます。合致するセルのCellオブジェクトが’返されます。


```
 In [2]: # %load c14_find_cell.py
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: cell = ws.find("2022/02/01")
    ...:
    ...: v1 = f"Found at Row:{cell.row} Col:{cell.col}"
    ...:

 In [3]: v1
 Out[3]: 'Found at Row:2 Col:1'

 In [4]:

```

Cellオブジェクトには、 `row` と  `col` の座標を表す属性があります。

 `find()` メソッドは最初に見つけたセルのCellオブジェクトを返します。複数に合致する場合は、 `findall()` メソッドを使用します。


```
 In [2]: # %load c15_findall.py
    ...: import re
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: regexp = re.compile(r'2022/.*/01')
    ...: cell_list = ws.findall(regexp)
    ...:
    ...:

 In [3]: cell_list
 Out[3]:
 [<Cell R1C1 '2022/01/01'>,
  <Cell R2C1 '2022/02/01'>,
  <Cell R3C1 '2022/03/01'>,
  <Cell R4C1 '2022/04/01'>,
  <Cell R5C1 '2022/05/01'>,
  <Cell R6C1 '2022/06/01'>,
  <Cell R7C1 '2022/07/01'>,
  <Cell R8C1 '2022/08/01'>,
  <Cell R9C1 '2022/09/01'>,
  <Cell R10C1 '2022/10/01'>,
  <Cell R11C1 '2022/11/01'>,
  <Cell R12C1 '2022/12/01'>]

 In [4]:

```

この例のように、 `find()` および　 `findall()` は正規表現に合致するセルを検索することが’できます。



## セルの書式

 `format()` メソッドを使用するとセルの書式を指定することができます。


```
 In [2]: # %load c16_formatting.py
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: _ = ws.format('A1:A12', {'textFormat': {'bold': True}})
    ...: # _ = ws.format('A1:A12', {'textFormat': {'bold': False}})
    ...:

 In [3]:

```


![](https://gyazo.com/78275a6399467adae9e04835e859402e.png)

## その他の操作
ここまでで、もう基本的な操作はできるようになります。他にも以下のようなメソッドが提供されています。

- **行の追加/挿入/削除**
  -  `append_row()` 　ー　最後に行を追加
  -  `append_rows()` ー　最後に複数の行を追加
  -  `insert_row()` ー　行を指定した位置に挿入
  -  `insert_rows()` ー　複数の行を指定した位置に挿入
  -  `delete_row()` ー　指定した行を削除
  -  `delete_rows()` ー 指定した位置から複数の行を削除

- **列の追加/挿入/削除**
  -  `add_cols()` ー　最後に複数の行を追加
  -  `insert_cols()` ー　複数の行を指定した位置に挿入
  -  `delete_columns()` ー 指定した位置から複数の行を削除


## 数式の処理

 `acell()` や  `cell()` に与えるキーワード引数  `value_render_option` の値により読み込み内容が異なります。


```
 In [2]: # %load c17_get_formula.py
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: v1 = ws.acell('D1').value
    ...: v2 = ws.acell('D1', value_render_option='FORMULA').value
    ...:

 In [3]: v1
 Out[3]: '130'

 In [4]: v2
 Out[4]: '=SUM(B1:C1)'

 In [5]:

```

デフォルトでは、数式が評価された結果の値が返されますが、 `value_render_option='FORMULA'` を与えると、数式が返されます。

セルを更新する場合では、数式を記述したいときは、 `raw=False` を与える必要があります。デフォルトでは、与えたデータがそのままセルの値となります。


```
 In [2]: # %load c18_put_formula.py
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: _ = ws.update('B13', '=AVERAGE(B1:B12)', raw=False)
    ...: _ = ws.update('C13', '=AVERAGE(C1:C12)')
    ...:
    ...: v1 = ws.acell('B13').value
    ...: v2 = ws.acell('B13', value_render_option='FORMULA').value
    ...: v3 = ws.acell('C13').value
    ...: v4 = ws.acell('C13', value_render_option='FORMULA').value
    ...:

 In [3]: v1
 Out[3]: '65'

 In [4]: v2
 Out[4]: '=AVERAGE(B1:B12)'

 In [5]: v3
 Out[5]: '=AVERAGE(C1:C12)'

 In [6]: v4
 Out[6]: '=AVERAGE(C1:C12)'

 In [7]:

```


## Gogle Finance からデータを読みだす
Google Spreadsheets では `GOOGLEFINANCE()` 関数を使うことができます。これを利用すると、Google Finance から現在や過去の証券や為替の各種情報を取得することができます。


```

 In [2]: # %load c19_google_finance.py
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: formula = '=GoogleFinance("currency:USDJPY", "average")'
    ...: _ = ws.update('B14', formula, raw=False)
    ...:
    ...: v1 = ws.acell('B14').value
    ...:

 In [3]: v1
 Out[3]: '121.969'

 In [4]:

```

 `GOOGLEFINANCE()` 関数の使用方法については、"[Google Spreadsheets で Google Finance  のデータを読み出してみよう]" を参照してください。

## ARRAYFORMULA()関数
[ARRAYFORMULA() ](https://support.google.com/docs/answer/3093275) は定義したセルより下のセルに関数を適用してくれます。


```
 In [2]: # %load c20_arrayformula.py
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet
    ...:
    ...: formula = '=ArrayFormula(B1:B12>60, "Upper", "Lower")'
    ...: _ = ws.update('E1', formula, raw=False)
    ...:

 In [3]:

```

この例の場合、セルF1に書き込まれた `ArrayFormula()` が　 `IF(...)` を下に続くセルに適用して展開します。途中のセルに文字列などが入力済みだとエラーになります。

## IMAGE()関数
[IMAGE()関数　 ](https://support.google.com/docs/answer/3093333?hl=ja)　はセルに指定したURL、もしくはURLが記述されているセルを与えると、セルに画像を挿入します。


```
 In [2]: # %load c21_image.py
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート1").worksheet
    ...: _ = ws.clear()
    ...:
    ...: image_url='https://www.google.com/images/srpr/logo3w.png'
    ...:
    ...: A_cells = ws.range("A1:A5")
    ...: for n, cell in enumerate(A_cells):
    ...:     cell.value = f'=Image(B{n+1})'
    ...:
    ...: B_cells = ws.range("B1:B5")
    ...: for cell in B_cells:
    ...:     cell.value = image_url
    ...:
    ...: _ = ws.update_cells(B_cells)
    ...: _ = ws.update_cells(A_cells, value_input_option="USER_ENTERED")
    ...:

 In [3]:

```

![](https://gyazo.com/3d7a360ef02caf9c9387be62429093fe.png)


## テキストをGoogle翻訳で変換する

同様に  `GoogleTranslate()` を呼び出すと、Google翻訳を利用することもできます。

 `GOOGLETRANSLACE(セル, ソース言語, ターゲット言語)`


```
 In [2]: # %load c20_goofle_translate.py
    ...: from gspread_utils import GSpread
    ...:
    ...: US_constitution = """\
    ...: We the People of the United States, in Order to form a more perfect Unio
    ...: n, establish Justice, insure domestic Tranquility, provide for the commo
    ...: n defense, promote the general Welfare, and secure the Blessings of Libe
    ...: rty to ourselves and our Posterity, do ordain and establish this Constit
    ...: ution for the United States of America."""
    ...:
    ...: ws = GSpread("PythonOsaka_tempfile").worksheet
    ...:
    ...:
    ...: _ = ws.clear()
    ...: _ = ws.update('A1', [[ US_constitution ]])
    ...:
    ...: formula = f'=GoogleTranslate(A1, "en", "ja")'
    ...: _ = ws.update('B1', formula, raw=False)
    ...:
    ...: v1 = ws.acell('B1').value
    ...:

 In [3]: v1
 Out[3]: '私たちの人々の人々は、より完璧な組合を形成するために、正義を確立し、国内の静けさを確立し、一般的な防衛を提供し、一般的な福祉を促進し、そして自信と私たちの後者の祝福を確実にし、聖職者との祝福を確実にします。アメリカ合衆国のためにこの憲法を確立する。'

 In [4]:

```

## Google Colab から Google Spreadsheets を利用する
Google Colab  から Google Spreadsheets  を利用することで、データーリソースとして利用できるようになり利便性がよくなります。

まず、Google Colab のセルで次コードを実行します。

 c90_google_colab.py
```
 from google.colab import auth
 from oauth2client.client import GoogleCredentials
 import gspread

 auth.authenticate_user()
 gc = gspread.authorize(GoogleCredentials.get_application_default())

```

  - このコードを実行すると、認証のためのURLが表示されるのでクリック
  - Google側の認証画面で、認証を行います。
  - 認証が完了すると verification code が表示されるのでそれをコピー
  - コピーしたcodeをColab側に貼り付ければ、それで認証は完了します

## 制約事項
PROXYを超えてアクセスする場合は、環境変数  `http_proxy` と  `https_proxy` をセットしている必要があります。

Google Cloud Platform の管理コンソール上で確認した時のデフォルトの制限値は以下の通りです。

- Drive API
  - API実行回数(日)	1,000,000,000回
  - API実行回数(100秒単位)	20,000回
  - API実行回数(100秒/ユーザー単位)	20,000回
- Spreadsheets API
  - API実行回数(日)	1,000,000,000回
  - API実行回数(100秒単位)	20,000回
  - API実行回数(100秒/ユーザー単位)	20,000回


## マクロ
Google Spreadsheets では Google App Script でマクロを記述します。インポートするExcelファイルにマクロがあるときは、
[Macro Convertor ](https://workspace.google.com/marketplace/app/macro_converter/383201976440?hl=ja)を試してみてください。

## まとめ

gspread を使用することで、簡単に Google Spreadsheets にアクセスできるようになります。そして、Google Colab やFlask、Django などのアプリケーションのバックエンドストレージとしても利用できることになるわけです。


## 参考

- Google Spreadsheets
  - [Spreadsheets API ](https://developers.google.com/sheets/api)
  - [Microsoft Excel から Google スプレッドシートへの移行 ](https://support.google.com/docs/answer/9331278?hl=ja&ref_topic=9296611&visit_id=637842027421041599-1782718943&rd=1)
  - [Google Finance ](https://support.google.com/docs/answer/3093281?hl=ja)

- gspread
  - [PyPI - gspread ](https://pypi.org/project/gspread/)
  - [ソースコード　](https://github.com/burnash/gspread)
  - [公式ドキュメント　](https://gspread.readthedocs.io/en/latest/)

- gspread10
  - [PyPI - gspread10 ](https://pypi.org/project/gspread10/)
  - [ソースコード ](https://github.com/abhi10sharma/Gspread-Sheets)

- gspread-rpa
  - [PyPI - gspread-rpa ](https://pypi.org/project/gspread-rpa/)
  - [ソースコード　](https://github.com/unipartdigital/gspread_rpa)

- gspread-formatting - セルの書式設定が簡単になる
  - [PyPI - gspread-formatting ](https://pypi.org/project/gspread-formatting/)
  - [ソースコード ](https://github.com/robin900/gspread-formatting)

- gspread-dataframe - Pandas DataFrame との連携が簡単になる
  - [PyPI - gspread-dataframe ](https://pypi.org/project/gspread-dataframe/)
  - [ソースコード ](https://github.com/robin900/gspread-dataframe)

- gspread-pandas　- Pandas DataFrame との連携が簡単になる
  - [PyPI - gspread-pandas ](https://pypi.org/project/gspread-pandas/)
  - [ソースコード ](https://github.com/aiguofer/gspread-pandas)

- 類似プロジェクト
  - [PyPI - gsheets ](https://pypi.org/project/gsheets/)
  - [PyPI - EZSheets ](https://pypi.org/project/EZSheets/)
  - [PyPI - pygsheets ](https://pypi.org/project/pygsheets/)
