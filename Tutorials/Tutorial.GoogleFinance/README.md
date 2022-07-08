GoogleSpreadsheetsでGoogleFinanceのデータを読み出してみよう
=================
![](https://gyazo.com/c4daada535f10df102b3af1b54f94c82.png)

## はじめに
米国株は日本株のような1単元（100株）での購入というのではなく、ほとんどの銘柄で1株から購入できるようになっています。米国株を扱う証券会社も増えたことから米国株をGoogle Financeで調べる機会も多くなったのではないでしょうか。
Google Spreadsheets で使用できる `GOOGLEFINANCE()` 関数は、 [Google Finance ](https://www.google.com/finance/?hl=ja) からデータを取得することができます。
この資料は、この `GOOGLEFINANCE()` 関数の使用方法について説明したものです。
Google Spreadsheets へのPython からアクセスする方法については、"[PythonでGoogleSpreadsheetsを読み書きしてみよう]" も参照してください。


## Google Finance について
Google Financeは、現在の市場情報を表示し、ビジネスニュースを集約したGoogleのサービスです。Google 検索と統合されていて、指定した企業名、ティッカーシンボルを検索することでその証券の現在の株価と過去のデータ、関連するニュースがすぐに表示されます。
2011年に Google Finance API の提供が廃止されたため、Google Finance で提供している株価や為替の情報を取得するための公式で唯一の方法が、Google Spreadsheets で  `GOOGLEFINANCE()` 関数を利用することです。

## GOOGLEFINANCE関数

 `GOOGLEFINANCE()` 関数の呼び出し方は次のようなになります。

 `GOOGLEFINANCE( tiker, attribute, start_date, end_date, interval )` 

  -  `ticker` ー ティッカーシンボルを与えます。
  -  `attibute` ー　属性
  -  `start_date` 　ー　開始日
  -  `end_date` 　ー　終了日
  -  `interval` ー 収集間隔

 `ticker` はティッカーシンボル(Ticker Symbol) を与えます。これは、企業が株式市場に上場する際に持つコードです。例えば、Apple は AAPL、マイクロソフトでは MSFT といったように割り当てられています。日本では証券コードとして4桁の数値が割り当てられています。選んだ銘柄が上場している証券取引所を指定することもできます。 例えばマイクロソフトはNASDAQに情報しているため、 `NASDAQ:MSFT` とします。日経平均は `INDEXNIKKEI:NI225` 、TOPIXは `NDEXTOPIX:TOPIX` で取得できますが、日本の東京証券取引所に上場している個別株を指定してもエラーになります。為替のシンボル’を与えることもできます。米ドルー日本円は  `currency:USDJPY` です。

 `attibute` は表示させたい属性を指定します。デフォルトは  `"price"` (価格)です。次のようなものを与えることができます。

  -  `price` ー 特定の銘柄のリアルタイムの価格
  -  `volume` ー　 現在の取引量
  -  `high` ー　現在または選択した日の高値
  -  `low` ー 現在または選択された日の安値
  -  `volumeavg` ー　1日の平均取引量
  -  `all` ー 上記5つの属性を指定したことと同じで
  -  `pe` ー 株価収益率(PER: Price to Earnings Ratio)
  -  `eps` ー　1株当たり純利益（EPS：Earnings Per Share）

現在のデータを使うか、過去のデータを使うかによって、表示できる属性が異なることに注意してください。現在のデータは15分ごとに更新されるので、完全にリアルタイムではないことに留意してください。

 `start_date` は、ヒストリカルデータ（Histrical Data : 過去のデータ）を使用するときに与えます。
 `TODAY()` もしくは与えないでおくと、リアルタイムデータを表示することができます。
 `end_date` は、終了日または開始日からの日数を指定します。与えないでおくと、1日分のデータが返されます。

 `interval` は間隔を指定します、データの粒度を表します。 `"DAILY"` か  `"WEEKLY"` を与えることがでます。

Google Spreadsheets はこれらを文字列として扱うため、2重引用符（ `"..."` )で囲む必要があることに注意してください。


## 株価データの取得
GAFAMと略称される Alphabet(Google)、Amazon、Meta(Facebook)、Apple、Microsoft の5社は、世界でも時価総額の高い上場企業5社で、市場に与える影響が大きいことで知られてます。
この GAFAM のデータを集めてみましょう。

![](https://gyazo.com/19e29cfaee9c410e143f1fbdd0d5b2d0.png)


gspreaed を使用するので、次のラッパーモジュールを用意しておきます。

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

コード中にハードコーディングしてもよいのですが、とりあえず、取得する企業とティッカーシンボルを格納したCSVファイルを用意します。

 bash
```
 $ cat GAFAM.csv
 Name,Ticker
 Alphabet,GOOGL
 Apple,AAPL
 Meta,FB
 Amazon,AMZN
 Microsoft,MSFT
 
```

与えたCSVファイルから `GOOGLEFINANCE()` の式を埋め込んだDataFrameを返す関数  `read_ticker()` としてみます。


```
 In [2]: # %load c01_get_symbols.py
    ...: from dataclasses import dataclass
    ...: import pandas as pd
    ...:
    ...: @dataclass
    ...: class GFinance(object):
    ...:     name: str
    ...:     ticker: str
    ...:
    ...:     def get_formula(self, attribute="price"):
    ...:         return f'=GoogleFinance("{self.ticker}", "{attribute}")'
    ...:
    ...: def read_ticker(csv_file=None):
    ...:     companies = pd.read_csv(csv_file)
    ...:     companies['Price'] = [GFinance(c[1], c[2]).get_formula()
    ...:                              for c in companies.itertuples()]
    ...:     return companies
    ...:
    ...: # df = read_ticker('GAFAM.csv')
    ...:
 
 In [3]: df = read_ticker('GAFAM.csv')
 
 In [4]: df
 Out[4]:
         Name Ticker                             Price
 0   Alphabet  GOOGL  =GoogleFinance("GOOGL", "price")
 1      Apple   AAPL   =GoogleFinance("AAPL", "price")
 2       Meta     FB     =GoogleFinance("FB", "price")
 3     Amazon   AMZN   =GoogleFinance("AMZN", "price")
 4  Microsoft   MSFT   =GoogleFinance("MSFT", "price")
 
 In [5]:
 
```

これを使ってスプレッドシートに書き出してみましょう。


```
 In [2]: # %load c02_load_price.py
    ...: import gspread_dataframe as gd
    ...: from gspread_utils import GSpread
    ...: from c01_get_symbols import read_ticker
    ...:
    ...: ws = gs = GSpread('PythonOsaka_tempfile').worksheet
    ...: _ = ws.clear()
    ...:
    ...: df = read_ticker('GAFAM.csv')
    ...: gd.set_with_dataframe(ws, df)
    ...:
 
 In [3]:
 
```

![](https://gyazo.com/7f894b23ece39cfd530c2eba0c72a1b5.png)

きちんと読み込めていますね。

このワークシートを読み込めばGoogleFinanceのデータを取得できたことになります。


```
 In [2]: # %load c03_get_price.py
    ...: import gspread_dataframe as gd
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = gs = GSpread('PythonOsaka_tempfile').worksheet
    ...:
    ...: all_rows = ws.get_all_values()
    ...: columns = all_rows.pop(0)
    ...: max_rows = len(all_rows)
    ...: df = gd.get_as_dataframe(ws,
    ...:               dtype={0: str, 1:str, 2:float},
    ...:               evaluate_formulas=True,
    ...:               nrows=max_rows, usecols=columns)
    ...:
    ...:
 
 In [3]: df
 Out[3]:
         Name Ticker    Price
 0   Alphabet  GOOGL  2781.35
 1      Apple   AAPL   174.61
 2       Meta     FB   222.36
 3     Amazon   AMZN  3259.95
 4  Microsoft   MSFT   308.31
 
 In [4]:
 
```



## ティッカーシンボルをセルから読み取る
ここまでは、 `GOOGLEFINANCE()` の引数としてティッカーシンボルを明示的に与えていましたが、じつはセルから読み込むこともできます。 


```
 In [2]: # %load c04_read_ticker_from_cell.py
    ...: import pandas as pd
    ...: import gspread_dataframe as gd
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread('PythonOsaka_tempfile').worksheet
    ...: _ = ws.clear()
    ...:
    ...: df = pd.read_csv('GAFAM.csv')
    ...:
    ...: start_col = 2
    ...: max_row = len(df)
    ...: formula = [ f'=GoogleFinance(C{x + start_col},"price")'
    ...:                     for x in range(max_row)]
    ...: df['Price'] = formula
    ...:
    ...: _ = gd.set_with_dataframe(ws, df, row=1, col=start_col)
    ...:
    ...: all_rows = ws.get_all_values()
    ...: columns = all_rows.pop(0)
    ...: max_rows = len(all_rows)
    ...:
    ...: df = gd.get_as_dataframe(ws,
    ...:               dtype={0: str, 1: str, 2:float},
    ...:               nrows=max_rows, usecols=[1,2,3],
    ...:               evaluate_formulas=True)
    ...:
 
 In [3]: df
 Out[3]:
         Name Ticker    Price
 0   Alphabet  GOOGL  2803.01
 1      Apple   AAPL   174.31
 2       Meta     FB   224.85
 3     Amazon   AMZN  3271.20
 4  Microsoft   MSFT   309.42
 
 In [4]: formula
 Out[4]:
 ['=GoogleFinance(C2,"price")',
  '=GoogleFinance(C3,"price")',
  '=GoogleFinance(C4,"price")',
  '=GoogleFinance(C5,"price")',
  '=GoogleFinance(C6,"price")']
 
 In [5]:
 
```

![](https://gyazo.com/1564e25367706ee5cd3bf20a4e176f1d.png)


ここまでは、 `"price"` の属性情報しか取得してきませんでした。OHLC(Open High Low Close: 4本値）や取引量を見たいときは、これまでのように個別に `"price"` や `"high"` など個別に属性を指定する場合は、つぎのようになります。


```
 In [2]: # %load  c05_get_multi_attributes.py
    ...: import pandas as pd
    ...: import gspread_dataframe as gd
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread('PythonOsaka_tempfile').worksheet
    ...: _ = ws.clear()
    ...:
    ...: df = pd.read_csv('GAFAM.csv', index_col=0)
    ...:
    ...: df2 = df.T
    ...:
    ...: attributes = ["price", "high", "low", "volume", "volumeavg", "pe", "eps"
    ...:  ]
    ...: for y in attributes:
    ...:     row = [f'=GoogleFinance("{x}", "{y}")'  for x in df2.loc['Ticker']]
    ...:     df2.loc[y] = row
    ...:
    ...: start_col = 2
    ...: _ = gd.set_with_dataframe(ws, df2, include_index=True, row=1, col=start_
    ...: col)
    ...:
    ...: all_rows = ws.get_all_values()
    ...: columns = all_rows.pop(0)
    ...: max_rows = len(all_rows)
    ...:
    ...: df3 = gd.get_as_dataframe(ws,
    ...:               nrows=max_rows, usecols=[1,2,3,4,5,6],
    ...:               index_col=0,
    ...:               evaluate_formulas=True)
    ...:
 
 In [3]: df3
 Out[3]:
           Alphabet     Apple      Meta   Amazon Microsoft
 Ticker       GOOGL      AAPL        FB     AMZN      MSFT
 price      2803.01    174.31    224.85   3271.2    309.42
 high       2809.42    174.88    227.28  3316.54    310.13
 low        2766.15    171.94     222.7  3246.39    305.54
 volume     1297072  78751328  19544758  2854475  27110529
 volumeavg  1702114  94753161  33844141  3512439  33492799
 pe           24.98     28.94     16.33    50.49     32.92
 eps          112.2      6.02     13.77    64.78       9.4
 
 In [4]: df2['Alphabet']
 Out[4]:
 Ticker                                      GOOGL
 price            =GoogleFinance("GOOGL", "price")
 high              =GoogleFinance("GOOGL", "high")
 low                =GoogleFinance("GOOGL", "low")
 volume          =GoogleFinance("GOOGL", "volume")
 volumeavg    =GoogleFinance("GOOGL", "volumeavg")
 pe                  =GoogleFinance("GOOGL", "pe")
 eps                =GoogleFinance("GOOGL", "eps")
 Name: Alphabet, dtype: object
 
 In [5]:
 
```

![](https://gyazo.com/e2991586e319c28c86bb999c2826c5ac.png)
 `GOOGLEFINANCE()` がサポートしている属性の詳細は、[ドキュメント ](https://support.google.com/docs/answer/3093281?hl=ja) を参照してください。

これも引数に与える値をセルから読み取らせることもできます。


```
 
 In [2]: # %load c06_get_multi_attributes_from_cell.py
    ...: import pandas as pd
    ...: import gspread_dataframe as gd
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread('PythonOsaka_tempfile').worksheet
    ...: _ = ws.clear()
    ...:
    ...: df = pd.read_csv('GAFAM.csv', index_col=0)
    ...:
    ...: df2 = df.T
    ...:
    ...: attributes = ["price", "high", "low", "volume", "volumeavg", "pe", "eps"
    ...:  ]
    ...:
    ...: ref_cols = ['C', 'D', 'E', 'F', 'G' ]
    ...: for y in range(len(attributes)):
    ...:     row = [f'=GoogleFinance({x}$2, B${y+3})'  for x in ref_cols]
    ...:     df2.loc[attributes[y]] = row
    ...:
    ...: start_col = 2
    ...: _ = gd.set_with_dataframe(ws, df2, include_index=True, row=1, col=start_
    ...: col)
    ...:
    ...: all_rows = ws.get_all_values()
    ...: columns = all_rows.pop(0)
    ...: max_rows = len(all_rows)
    ...:
    ...: df3 = gd.get_as_dataframe(ws,
    ...:               nrows=max_rows, usecols=[1,2,3,4,5,6],
    ...:               index_col=0,
    ...:               evaluate_formulas=True)
    ...:
 
 In [3]: df3
 Out[3]:
           Alphabet     Apple      Meta   Amazon Microsoft
 Ticker       GOOGL      AAPL        FB     AMZN      MSFT
 price      2803.01    174.31    224.85   3271.2    309.42
 high       2809.42    174.88    227.28  3316.54    310.13
 low        2766.15    171.94     222.7  3246.39    305.54
 volume     1297072  78751328  19544758  2854475  27110529
 volumeavg  1702114  94753161  33844141  3512439  33492799
 pe           24.98     28.94     16.33    50.49     32.92
 eps          112.2      6.02     13.77    64.78       9.4
 
 In [4]: df2['Alphabet']
 Out[4]:
 Ticker                          GOOGL
 price        =GoogleFinance(C$2, B$3)
 high         =GoogleFinance(C$2, B$4)
 low          =GoogleFinance(C$2, B$5)
 volume       =GoogleFinance(C$2, B$6)
 volumeavg    =GoogleFinance(C$2, B$7)
 pe           =GoogleFinance(C$2, B$8)
 eps          =GoogleFinance(C$2, B$9)
 Name: Alphabet, dtype: object
 
 In [5]: df2['Apple']
 Out[5]:
 Ticker                           AAPL
 price        =GoogleFinance(D$2, B$3)
 high         =GoogleFinance(D$2, B$4)
 low          =GoogleFinance(D$2, B$5)
 volume       =GoogleFinance(D$2, B$6)
 volumeavg    =GoogleFinance(D$2, B$7)
 pe           =GoogleFinance(D$2, B$8)
 eps          =GoogleFinance(D$2, B$9)
 Name: Apple, dtype: object
 
 In [6]:
 
```

![](https://gyazo.com/305b58f88fed41d4ff6286001777e319.png)

ただし、この方法は実際にスプレッドシートを操作するときは非常に便利なのですが、コードでは可読性が悪くなるので注意してください。

## 特定期間のデータを取得
「コロナショック」として知られる2020年02月24日から1週間の下落は、過去の危機に匹敵する記録的な株価下落で、24～28日のダウ平均の下落率は12%を超え、2008年のリーマンショックの金融危機以降で「最悪の一週間」でした。
そういった特定の週の日次終値を表示したい場合は、 `GOOGLEFINANCE()` 関数の3番目と4番目の引数で日付範囲を指定します。
Alphabet社の株価がどのように推移したのかをみてみましょう。


```
 In [2]: # %load c10_covid19_shock.py
    ...: import gspread_dataframe as gd
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread('PythonOsaka_tempfile').worksheet
    ...: _ = ws.clear()
    ...:
    ...: formula = (
    ...:     '=GOOGLEFINANCE("GOOGL","price"'
    ...:     ',DATE(2020,2,24),DATE(2020,2,29))'
    ...:     )
    ...: _ = ws.update('B1', formula, raw=False)
    ...:
    ...: all_rows = ws.get_all_values()
    ...: columns = all_rows.pop(0)
    ...: max_rows = len(all_rows)
    ...:
    ...: df = gd.get_as_dataframe(ws,
    ...:               dtype={0: str, 1:float},
    ...:               nrows=max_rows, usecols=[1,2],
    ...:               parse_dates=['Date'],
    ...:               evaluate_formulas=True)
    ...:
 
 In [3]: df
 Out[3]:
                  Date    Close
 0 2020-02-24 16:00:00  1419.86
 1 2020-02-25 16:00:00  1386.32
 2 2020-02-26 16:00:00  1390.47
 3 2020-02-27 16:00:00  1314.95
 4 2020-02-28 16:00:00  1339.25
 
 In [4]:
 
```

![](https://gyazo.com/f118672c3f9cd8ed222096fec868f92f.png)


ここでのポイントは2つです。

- 1つのセルに書き出した `GOOGLEFINANCE()` 関数が評価されると、続くセルを占有する
- 日付のデータは内部的には数値として管理されていて、日付として表示されるかどうかは書式依存する

この例の場合では、もしセルB2にデータが存在していると、 `GOOGLEFINANCE()` 関数が展開できないためエラーになり、 `get_as_dataframe()` で読み出しても `Date` カラムが存在しないことから `ValueError` の例外が発生します。

次に、日付データについてです。ExcelやGoogle Spreadsheet では日付は内部的には数値として保持しています。そして、gspread の  `clear()` はデータはクリアしますが、書式をクリアしないことに注意が必要です。前述のコードは新規作成したシートではセルの書式はデータから自動推定されるため、期待通りに動作しますが、書式が設定されている既存のスプレッドシートではうまくいかない場合があります。
スプレッドシート側で列Bを数値としてから、先のコードを実行すると、次のような結果になってしまいます。


```
 In [2]: # %load c11_covid19_shock.py
    ...: import gspread_dataframe as gd
    ...: from gspread_utils import GSpread
    ...:
    ...: ws = GSpread('PythonOsaka_tempfile').worksheet
    ...: _ = ws.clear()
    ...:
    ...: formula = (
    ...:     '=GOOGLEFINANCE("GOOGL","price"'
    ...:     ',DATE(2020,2,24),DATE(2020,2,29))'
    ...:     )
    ...: _ = ws.update('B1', formula, raw=False)
    ...:
    ...: all_rows = ws.get_all_values()
    ...: columns = all_rows.pop(0)
    ...: max_rows = len(all_rows)
    ...:
    ...: df = gd.get_as_dataframe(ws,
    ...:               dtype={0: str, 1:float},
    ...:               nrows=max_rows, usecols=[1,2],
    ...:               parse_dates=['Date'],
    ...:               evaluate_formulas=True)
    ...:
 
 In [3]: df
 Out[3]:
                 Date    Close
 0  43885.66666666667  1419.86
 1  43886.66666666667  1386.32
 2  43887.66666666667  1390.47
 3  43888.66666666667  1314.95
 4  43889.66666666667  1339.25
 
 In [4]:
 
```

![](https://gyazo.com/ebbaabf56e69f0825fb5e94863bfe61b.png)

Python から　スプレッドシートの書式を設定する場合は、gspread-formatting を使用すると簡単になります。このライブラリは、gspread-dataframe を開発した [Robin Thomas氏  https://github.com/robin900] が開発したもので、Google Spreadsheetsの [Sheets API ](https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#CellFormat) をすべてサポートしています。


```
 In [2]: # %load c11_covid19_shock_with_format.py
    ...: import gspread_dataframe as gd
    ...: import gspread_formatting as gf
    ...: from gspread_utils import GSpread
    ...:
    ...: _TICKER = 'GOOGL'
    ...: _START = 'DATE(2020,2,24)'
    ...: _END = 'DATE(2020,2,29)'
    ...:
    ...: ws = GSpread('PythonOsaka_tempfile').worksheet
    ...: _ = ws.clear()
    ...: date_formats = gf.cellFormat(
    ...:                    numberFormat=gf.numberFormat(
    ...:                                type='DATE',
    ...:                                pattern='YYYY/MM/DD hh:mm'))
    ...: _ = gf.set_column_width(ws, 'B', 120)
    ...: _ = gf.format_cell_range(ws, 'B', date_formats)
    ...: cells = ws.range('B2:B6')
    ...: _ = ws.update_cells(cells, value_input_option='USER_ENTERED')
    ...:
    ...: formula = (
    ...:     f'=GOOGLEFINANCE("{_TICKER}","price"'
    ...:     f',{_START},{_END})'
    ...:     )
    ...: _ = ws.update('B1', formula, raw=False)
    ...:
    ...: all_rows = ws.get_all_values()
    ...: columns = all_rows.pop(0)
    ...: max_rows = len(all_rows)
    ...:
    ...: df = gd.get_as_dataframe(ws,
    ...:               dtype={0: str, 1:float},
    ...:               nrows=max_rows, usecols=[1,2],
    ...:               parse_dates=['Date'],
    ...:               evaluate_formulas=True)
    ...:
 
 In [3]: df
 Out[3]:
                  Date    Close
 0 2020-02-24 16:00:00  1419.86
 1 2020-02-25 16:00:00  1386.32
 2 2020-02-26 16:00:00  1390.47
 3 2020-02-27 16:00:00  1314.95
 4 2020-02-28 16:00:00  1339.25
 
 In [4]:
 
```


ここで、書式は `GOOGLEFINANCE()` をセルに書き込む前に行うことがポイントです。


## 為替レートを取得する
Google Spreadsheetsの `GOOGLEFINANCE()` 関数のもう一つの優れた機能は、リアルタイムで為替レートを取得できることです。株式のティッカーシンボルと同様に、 `CURRENCY` の後に、 `USJPY` や  `EURJPY` などのように、変換したい2つの通貨のコードを入力することで、為替レートを取得することができます。また、日付を指定することで、過去のデータも取得することもできます。

USDJPYの為替レートを参照したい場合は、 `=GOOGLEFINANCE("CURRENCY:USDJPPY")` と入力します。返される値は、1米ドル( `USD` )に対する日本円( `JPY` )を表しています。


```
 In [2]: # %load c20_usdjpy.py
    ...: import gspread_dataframe as gd
    ...: import gspread_formatting as gf
    ...: from gspread_utils import GSpread
    ...:
    ...: _TICKER = 'currency:USDJPY'
    ...: _START = 'DATE(2022,2,1)'
    ...: _END = 'DATE(2022,3,31)'
    ...:
    ...: ws = GSpread('PythonOsaka_tempfile').worksheet
    ...: _ = ws.clear()
    ...: date_formats = gf.cellFormat(
    ...:                    numberFormat=gf.numberFormat(
    ...:                                type='DATE',
    ...:                                pattern='YYYY/MM/DD hh:mm'))
    ...: price_formats = gf.cellFormat(
    ...:                    horizontalAlignment='RIGHT',
    ...:                    numberFormat=gf.numberFormat(
    ...:                                type='TEXT',
    ...:                                pattern='###.000'))
    ...: _ = gf.set_column_width(ws, 'B', 120)
    ...: _ = gf.format_cell_range(ws, 'B', date_formats)
    ...: _ = gf.format_cell_range(ws, 'C', price_formats)
    ...:
    ...: cells = ws.range('B2:B64')
    ...: _ = ws.update_cells(cells, value_input_option='USER_ENTERED')
    ...:
    ...: formula = (
    ...:     f'=GOOGLEFINANCE("{_TICKER}","price"'
    ...:     f',{_START},{_END})'
    ...:     )
    ...: _ = ws.update('B1', formula, raw=False)
    ...:
    ...: all_rows = ws.get_all_values()
    ...: columns = all_rows.pop(0)
    ...: max_rows = len(all_rows)
    ...:
    ...: df = gd.get_as_dataframe(ws,
    ...:               dtype={0: str, 1:float},
    ...:               nrows=max_rows, usecols=[1,2],
    ...:               parse_dates=['Date'],
    ...:               evaluate_formulas=True)
    ...:
 
 In [3]: df.head()
 Out[3]:
                  Date     Close
 0 2022-02-01 23:58:00  114.7395
 1 2022-02-02 23:58:00  114.3700
 2 2022-02-03 23:58:00  114.9650
 3 2022-02-04 23:58:00  115.2250
 4 2022-02-05 23:58:00  115.2250
 
 In [4]: df.tail()
 Out[4]:
                   Date     Close
 53 2022-03-26 23:58:00  122.0950
 54 2022-03-27 23:58:00  122.2755
 55 2022-03-28 23:58:00  123.6740
 56 2022-03-29 23:58:00  123.1330
 57 2022-03-30 23:58:00  122.0655
 
 In [5]:
 
```

![](https://gyazo.com/78612aeedb513ac390f8cb38eda521f6.png)

## 日本の上場企業の株価を取得
 `GOOGLEFINANCE()` 関数は日本の上場企業のティッカーシンボルを与えるとエラーになりますが、Goofle Finance のサービスとしては受け付けています。そこで、 `IMPORTXML()` 関数を使ってスポットの株価を読みだすことはできます。ただし、3分間隔での更新される情報なのでリアルタイムというわけではありません。

例えば、トヨタの株価は次のように取得することができます。ティッカーシンボルの与え方に注意してください。


```
 In [2]: # %load c30_japanese_stock.py
    ...: from gspread_utils import GSpread
    ...:
    ...: _TICKER="7203:TYO"
    ...:
    ...: ws = GSpread('PythonOsaka_tempfile').worksheet
    ...: _ = ws.clear()
    ...:
    ...: formula = (
    ...:     f'=IMPORTXML("https://www.google.com/finance/quote/{_TICKER}",'
    ...:      '"//*[@class=\'YMlKec fxKbKc\']")'
    ...:     )
    ...:
    ...: _ = ws.update('B1', formula, raw=False)
    ...:
    ...: v1 = ws.acell('B1').value
    ...:
 
 In [3]: v1
 Out[3]: '¥2,217.50'
 
 In [4]:
 
```

この方法は、WEBサービスの株価データをスクレイピングしてることになります。データのスクレイピングすることを許可していないWEBサイトもあるため利用には注意が必要です。スクレイピングをする場合には、事前にサイトの利用規約や `robots.txt` をチェックして、データスクレイピングをしても問題ないかを確認した上で、データの取得を実行してください。
この資料作成時の[Googleの robots.txt  ](https://www.google.com/robots.txt) では、Google Finance は  `Allow` となっているため利用可能でした。



## Apps Script で関数を定義する
Pythonから使用するためには冗長ですが、Google Spreadsheets にカスタム関数を追加させることもできます。

[! 拡張機能]をクリックして、[! Apps Script] を選択

![](https://gyazo.com/0975fb3eb67dc5b86dbabcf5041d1933.png)

![](https://gyazo.com/ae77642aa513d05436648276644ee01b.png)



エディタが表示されるので次のコードを入力

 AppsScript
```
 /**
  * To get stock price from google finance
  * 
  * @param {number} code - stock code for Tokyo Exchange
  * @return stockprice
  * @customfunction
  */
 function TOKYO_STOCK_PRICE(code) {
   let url = 'https://www.google.com/finance/quote/' + code + ':TYO';
   let html = UrlFetchApp.fetch(url).getContentText();
   let stockPrice = Parser.data(html)
     .from('<div class="YMlKec fxKbKc">')
     .to('</div>')
     .build();
   console.log('StockPrice:'+stockPrice);
   return stockPrice;
 }
 
```

サイドメニューの[! ライブラリ]をクリック

![](https://gyazo.com/bf38094dad3aa87a9c4e24baec85c378.png)



![](https://gyazo.com/5e0a9474cbd4df528f5dace358c91e46.png)

ライブラリIDの入力を求められるので、次のIDを入力して、[! 検索]　をクリック

 ライブラリID
```
 1Mc8BthYthXx6CoIz90-JiSzSafVnT6U3t0z_W3hLTAX5ek4w0G_EIrNw
```

![](https://gyazo.com/c29b0aebfdcfce95d761b134c3b1ac81.png)
[! 追加]をクリックします。

![](https://gyazo.com/590fb45fb4dd59e193222c5d8ef0bee8.png)

[! ＞実行]　をクリックするとダイアログが表示されます。
![](https://gyazo.com/9935a384118e7c4a66db3a220b9364e0.png)

[! 権限を確認]　をクリックすると、[# アカウントの選択]画面に遷移するので、自分のアカウントをクリック
![](https://gyazo.com/209d7cccb88e3c2180aa3658f29c945b.png)



警告ダイアログが表示されるので、[! 詳細]　をクリック
![](https://gyazo.com/66b27949b909be996dd31426931705a7.png)


[! Untitled project（安全ではないページ）に移動] をクリックして、続くダイアログで　[! 許可]　をクリックします。

これで、このワークシートで  `TOKYO_STOCK_PRICE()` 関数が使えるようになります。

![](https://gyazo.com/350eb3e64f86b06450a1f263f64f9a08.png)


![](https://gyazo.com/180379219ae4ae0075bef4d8cc73237a.png)



```
 In [2]: # %load c31_custom_function.py
    ...: from gspread_utils import GSpread
    ...:
    ...: _TICKER="7203"
    ...:
    ...: ws = GSpread('PythonOsaka_tempfile').worksheet
    ...: _ = ws.clear()
    ...:
    ...: formula = f'=TOKYO_STOCK_PRICE({_TICKER})'
    ...:
    ...: _ = ws.update('B2', formula, raw=False)
    ...:
    ...: v1 = ws.acell('B2').value
    ...:
 
 In [3]: v1
 Out[3]: '¥2,179.50'
 
 In [4]:
 
```

## まとめ
Google Spreadsheetsで株式情報を管理する最大の利点は、Python や  `GoogleFinance()` 関数などの様々なデータ操作ツールを利用できることです。自分のポートフォリオの資産価値を把握することが簡単になります。


## 参考
- gspread
  - [PyPI - gspread ](https://pypi.org/project/gspread/)
  - [ソースコード  ](https://github.com/burnash/gspread)
  - [公式ドキュメント  ](https://gspread.readthedocs.io/en/latest/)
- gspread-dataframe
    - [PyPI - gspread-dataframe ](https://pypi.org/project/gspread-dataframe/)
    - [ソースコード ](https://github.com/robin900/gspread-dataframe)
- gspread-formatting
    - [PyPI - gspread-formatting ](https://pypi.org/project/gspread-formatting/)
    - [ソースコード ](https://github.com/robin900/gspread-formatting)
- Google Spreadsheet API
  - [Updating Sheet ](https://developers.google.com/sheets/api/guides/batchupdate) - セルフォーマットについて記載
- Google Spreadsheet 関数
  - [GOOGLEFINANCE関数  ](https://support.google.com/docs/answer/3093281?hl=ja)
  - [IMORTXML関数 ](https://support.google.com/docs/answer/3093342?hl=ja)
- Google Apps Script
  - [Parser ライブラリ ](https://script.google.com/home/projects/1Mc8BthYthXx6CoIz90-JiSzSafVnT6U3t0z_W3hLTAX5ek4w0G_EIrNw/edit)
- Wikipedia
  - [ISO4217 通過コード ](https://ja.wikipedia.org/wiki/ISO_4217)


