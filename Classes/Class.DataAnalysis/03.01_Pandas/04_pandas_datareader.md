pandas-datareaderを使ってみよう
=================
### pandas_datareader
CSVファイルやエクセルファイルなどをインターネットからダウンロードすることは、pandas だけでも行うことができますが、pandas_datareader を使うと、データソースへのアクセスをより簡単に行うことができるようになります。

### インストール
pandas_datareader は拡張モジュールなので次のようにインストールします。
 bash condaの場合
```
 $ conda install pandas-datareader
 bash pipの場合
```
 $ pip install pandas-datareader
```

### 利用準備
pandas-datareader のバージョンが 0.8.0 までには、
 `pandas_datareader` をインポートするとエラーになる場合があります。

Ipython
```
 In [1]: import pandas_datareader as pdr                                           
 /Users/goichiiisaka/anaconda3/envs/py36/lib/python3.6/site-packages/pandas_datareader/compat/__init__.py:7: FutureWarning: pandas.util.testing is deprecated. Use the functions in the public API at pandas.testing instead.
   from pandas.util.testing import assert_frame_equal
```

これは、 `pandas_datareader` で  `pandas` が非推奨にした `pandas.util.testing` を利用しているためです。
メッセージにあるように `pandas_datareader/compat/__init__.py` の7行目にある、
 `pandas.util.testing` を `pandas.testing` に修正するとこのメッセージが表示されなくなります。


```
 from distutils.version import LooseVersion
 import sys
 
 import pandas as pd
 from pandas.api.types import is_list_like, is_number
 import pandas.io.common as com
 from pandas.util.testing import assert_frame_equal
```


```
 from distutils.version import LooseVersion
 import sys
 
 import pandas as pd
 from pandas.api.types import is_list_like, is_number
 import pandas.io.common as com
 from pandas.testing import assert_frame_equal
```

pandas-datareader のバージョン 0.9.0 ではこの問題は修正済みです。

###  データソース
panda_datareader は次のデータソースからダウンロードをサポートしています。
データサイトによっては、APIキーが必要になるものがあります。

- [Tiingo ](https://www.tiingo.com/)
  - 株式、投資信託、ETFの過去の1日の終値をデータAPIに提供しています
  - APIキーを取得するには登録が必要です（無料）
  - 無料のアカウントはアクセスできるシンボル数に制限があります
- [IEX ](https://iextrading.com/)
  - Investors EXchange（IEX）は幅広いデータを提供しています
  - 過去の株価は最長15年間利用できます。 
  - IEX Cloud Consoleからの公開可能なAPIキーが必要です。
- [Alpha Vantage ](https://www.alphavantage.co/documentation)
  - Aリアルタイムの株式と外国為替データを提供しています。
  - APIキーを取得するには登録が必要です（無料）
- [Econdb ](https://www.econdb.com/)
  - 90以上の公式統計機関からの経済データを提供しています。
  - APIキーを取得するには登録が必要です（無料）
- [Enigma ](https://enigma.com/)
  - 構造化された公開データの世界最大のリポジトリ
- [Quandl ](https://www.quandl.com/)
  - 株式、投資信託、ETFの過去のデータを提供しています。
  - データの品質は必ずしも良いとは言えません。
- [FRED ](https://fred.stlouisfed.org/)
  - セントルイス連邦準備銀行の研究部門が管理するデータベース
  - 87のソースから500,000を超える経済時系列データを提供しています。
- [Fama/French http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html]
  - Kenneth French教授が自身のホームページで無料公開しているデータ
  - 市場ポートフォリオ、時価総額ファクター、簿価時価比率ファクター、無リスク金利のデータからなる
- [World Bank http://data.worldbank.org/]
  - 世界銀行が公開している世界開発指標(WDI:World Development Indicators)
- [OECD http://stats.oecd.org/]
  - 経済協力開発機構が公開している統計情報
- [Eurostat http://ec.europa.eu/eurostat/]
  - 欧州委員会で統計を担当する部局が公開する、欧州連合に関連する統計情報
- [TSP Fund Data ](https://www.tspfolio.com/thriftsavingsplan)
  - TSPは運用する投資ファンドのパフォーマンスの履歴とリスク特性を公開しています。
- [Nasdaq Trader Symbol Definitions http://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqtraded.txt]
  - NASDAQは株式の過去のデータを公開しています。
- [Stooq Index Data ](https://stooq.com/)
  - Stooqは、一般的なインデックスデータを公開しています。
  - 日本株のデータも取得することができます。例：トヨタ 7203.JP
- [MOEX Data ](https://www.moex.com/a1532)
  - モスクワ証券取引所は過去の株式のデータを公開しています。
- [Yahoo ](https://finance.yahoo.com/)
  - Yahoo Finance が公開している株式、為替の過去のデータ
  - 日本株のデータも取得することができます。例：トヨタ 7203.T

### 利用方法
Yahoo Finance からアップル社の株価データをダウンロードするときは、
次のように行います。

 pandas_datareader1.py
```
 from datetime import datetime
 import pandas as pd
 import pandas_datareader as pdr
 
 start=datetime(2010, 1, 1)
 end=datetime(2020, 1, 1)
 df = pdr.DataReader("AAPL", 'yahoo', start, end)
 
 print(df.head())
```



```
 In [2]: # %load pandas_datareader1.py 
    ...: from datetime import datetime 
    ...: import pandas as pd 
    ...: import pandas_datareader as pdr 
    ...:  
    ...: start=datetime(2010, 1, 1) 
    ...: end=datetime(2020, 1, 1) 
    ...: df = pdr.DataReader("AAPL", 'yahoo', start, end) 
    ...:  
    ...: print(df.head()) 
    ...:                                                                           
                  High        Low       Open      Close       Volume  Adj Close
 Date                                                                          
 2009-12-31  30.478571  30.080000  30.447144  30.104286   88102700.0  26.131752
 2010-01-04  30.642857  30.340000  30.490000  30.572857  123432400.0  26.538483
 2010-01-05  30.798571  30.464285  30.657143  30.625713  150476200.0  26.584366
 2010-01-06  30.747143  30.107143  30.625713  30.138571  138040000.0  26.161509
 2010-01-07  30.285715  29.864286  30.250000  30.082857  119282800.0  26.113146
```

### データをキャッシュする
拡張モジュール  `requests_cache` をインストールすると、ダウンロードしたデータをキャッシュすることができます。

 `requests_cache` は拡張モジュールなので次のようにインストールします。
 bash
```
 $ pip install requests_cache
```


 IPython
```
 In [2]: # %load pandas_datareader2.py 
    ...: from datetime import datetime, timedelta 
    ...: import pandas as pd 
    ...: import pandas_datareader as pdr 
    ...: from requests_cache import CachedSession 
    ...:  
    ...: expire_after = timedelta(days=3) 
    ...: session = CachedSession(cache_name='cache', backend='sqlite', 
    ...:                         expire_after=expire_after) 
    ...:  
    ...: start=datetime(2010, 1, 1) 
    ...: end=datetime(2020, 1, 1) 
    ...: df = pdr.DataReader("AAPL", 'yahoo', start, end, session=session) 
    ...:  
    ...: print(df.head()) 
    ...:                                                                           
                  High        Low       Open      Close       Volume  Adj Close
 Date                                                                          
 2009-12-31  30.478571  30.080000  30.447144  30.104286   88102700.0  26.131752
 2010-01-04  30.642857  30.340000  30.490000  30.572857  123432400.0  26.538483
 2010-01-05  30.798571  30.464285  30.657143  30.625713  150476200.0  26.584366
 2010-01-06  30.747143  30.107143  30.625713  30.138571  138040000.0  26.161509
 2010-01-07  30.285715  29.864286  30.250000  30.082857  119282800.0  26.113146
```

 `CachedSession()` に与えている  `backend='sqlite'` で、SQLiteデータベースに格納します。

 `DataReader()` を呼び出すときに、 `session=` でキャッシュ・セッションを与えておくと、
キャッシュにデータがあるときは、そこから読み込むようになります。
この例では、キャッシュは３日間保存されます。

参考：
- [Pandas-Datareader オフィシャルサイト ](https://pandas-datareader.readthedocs.io)



